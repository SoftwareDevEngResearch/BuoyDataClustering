# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 02:21:41 2019

@author: hanna
"""

# Wave Directionality study.
# This will analyze the directionality of waves with the wave height and period.
# test file with just analyze one year of buoy data from NOAA 46050 located at Newport, OR

# Values in full text file:
# YY  MM DD hh mm WDIR WSPD GST  WVHT   DPD   APD MWD   PRES  ATMP  WTMP  DEWP  VIS  TIDE
# units:
# yr  mo dy hr mn degT m/s  m/s     m   sec   sec deg    hPa  degC  degC  degC  nmi    ft


## Project Update:
# Updated by Hannah Mankle 4/30/19
# Update includes 2D k-means clustering of wave height & wave period
# These clusters will be optimized against tolerance & number of clusters
# data was cleaned further to emliminate outliers in the NOAA data

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import pairwise_distances_argmin
from sklearn.cluster import KMeans
from sklearn.neighbors import LocalOutlierFactor
from sklearn import preprocessing
import os
import glob

def combining_files(file_name, wave_files, combined_data=None):
    file_name = str(file_name)
    try:
        # print 'phase 2'
        with open('combined_data_' + file_name + '.txt', 'r') as f:
            d = []
            for line in f:
                d.append(line.split())
            d = np.array(d)
            # print d
            return d
    except:
        # print 'phase 1'
        with open('combined_data_' + file_name + '.txt', 'w') as outfile:
            for name in wave_files:
                with open(name) as infile:
                    for line in infile:
                        outfile.write(line)
        combining_files(file_name, buoy_files, combined_data)


def cleaning(file_name, wave_files, combined_data=None, cleaning_data=None):
    ## bug when trying to pass through this code on intial run when cleaning file is being made
    ## need to fix
    file_name = str(file_name)
    if os.path.exists('cleaning_data_' + file_name + '.txt'):
        with open('cleaning_data_' + file_name + '.txt', 'r') as f:
            df = pd.read_csv('cleaning_data_' + file_name + '.txt', dtype=float)
        df[['#YY', 'MM', 'DD', 'hh', 'mm']]\
            = df[['#YY', 'MM', 'DD', 'hh', 'mm']].astype(int)
        return df

    else:

        print 'test'
        d = combining_files(file_name, wave_files, combined_data=None)
        print d
        print "entering data_frame"
        df = pd.DataFrame(data=d[2:], columns=d[0])
        print df
        df_1 = df.loc[:, ('#YY', 'MM', 'DD', 'hh', 'mm', 'WVHT', 'APD', 'MWD')]
        # print df_1

        # get rid of extra column headers in dataframe
        df_1 = df_1[~df_1['#YY'].isin(['#YY', '#yr']) == True]
        # print df_1
        # rows with headers in them
        # df_3 = df_1[~df_1['#YY'].isin(['#YY', '#yr']) == False]
        # print df_3
        # Change type of dataFrame from objects to ints and floats
        df_1[['WVHT', 'APD', 'MWD']]\
            = df_1[['WVHT', 'APD', 'MWD']].astype(float)
        df_1[['#YY', 'MM', 'DD', 'hh', 'mm']]\
              = df_1[['#YY', 'MM', 'DD', 'hh', 'mm']].astype(int)
        # # Check the data types of the dataframe
        # print df_1.dtypes

        # cleans data of any NaNa
        df_1 = df_1.dropna(axis=0, how='any')
        # print df_1
        # Cleaning data of values of wave direction over 360 or below 0
        # Cleaning data of wave height values over 20 m
#        count = 0
        print 'entering first for loop'
        for index, row in df_1.iterrows():
            if row['MWD'] > 360.0:
                df_1.drop(index, inplace=True)
            if row['MWD'] < 0.0:
                df_1.drop(index, inplace=True)

            #     if 0.0 <= row['MWD'] <= 140.0:
            #         # checks to see how many outliers there are 
            #         # in the distribution
            #         count += 1
            # print 'below 140 degrees: ', count
            # print ''
        print 'reindexing'
        df_1 = df_1.reset_index(drop=True)

        print 'entering second for loop'
        for index, row in df_1.iterrows():
            if row['WVHT'] > 20.0:
                df_1.drop(index, inplace=True)

        print 'reindexing'

        print 'entering third for loop'
        for index, row in df_1.iterrows():
            if row['APD'] > 20.0:
                df_1.drop(index, inplace=True)

        print 'reindexing'
        
        ##cutting out the outlieers from dataframe
        print 'eliminating outliers'
        normalized_data = normalize(df_1)
        n_df = normalized_data[['WVHT', 'APD']]
        
        X = np.array(n_df.values, dtype = float)
        
        clf = LocalOutlierFactor(n_neighbors=1000, contamination=0.01)
        # use fit_predict to compute the predicted labels of the training samples
        # (when LOF is used for outlier detection, the estimator has no predict,
        # decision_function and score_samples methods).
        y_pred = clf.fit_predict(X)
        df_1.insert(loc=8, column= 'outlier', value=y_pred)
            
        for index, row in df_1.iterrows():
                if row['outlier'] == -1:
                    df_1.drop(index, inplace=True)
        

        with open('cleaning_data_' + file_name + '.txt', 'w') as f:
            df_1.to_csv('cleaning_data_' + file_name + '.txt', index=False)

        cleaning(file_name, wave_files, combined_data, cleaning_data)

# only run for Hawaii
def dir_cleaning(f_name, data):
    
    if str(f_name) == "HI_51202":
        df = cleaning(f_name, data)
#        print df
        df = df.sort_values(by=['MWD'])
        df_one = df[df.MWD < 250.0]
        # print 'df_hi_one ', df_hi_one
    
        df_two = df[df.MWD >= 250.0]
        df_two.is_copy = False
        df_two['MWD'] = df_two['MWD'].apply(lambda x: x-360.0)
        # print 'df_hi_two ', df_hi_two
    
        frames = [df_one, df_two]
        d = pd.concat(frames)
        d.sort_index(inplace=True)
        
    elif str(f_name) == "CA_46022":
        df = cleaning(f_name, data)
#        print df
        df = df.sort_values(by=['MWD'])
        df_one = df[df.MWD < 100.0]
        df_one.is_copy = False
        df_one['MWD'] = df_one['MWD'].apply(lambda x: x+360)
        # print 'df_one ', df_hi_one
    
        df_two = df[df.MWD >= 100.0]
        df_two.is_copy = False
        df_two['MWD'] = df_two['MWD'].apply(lambda x: x)
        # print 'df_two ', df_two
    
        frames = [df_one, df_two]
        d = pd.concat(frames)
        d.sort_index(inplace=True)
    return d

def compare(f_name, cleaned_data):
    dir_cleaning(f_name, cleaned_data)
    print"passed through HI function"
    print 'compare test'
    df = cleaned_data
#    print df['MWD'].describe()
#    print df['WVHT'].describe()
#    print df['APD'].describe()
    print 'binning data.....'
    b = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280,\
         300, 320, 340, 360]
    df_1 = df.groupby(pd.cut(df['MWD'], bins=b))
    # cleans data of any NaNa
#    print df_1['MWD', 'mm']

    df_1 = df_1.mean()
    df_1 = df_1[np.isfinite(df_1['MWD'])]

    # print 'binning data:'
    # print df_1
    return df_1

def normalize(df):
    x = df.values
    min_max_scale = preprocessing.MinMaxScaler()
    x_scaled = min_max_scale.fit_transform(x)
    df_scale = pd.DataFrame(x_scaled, columns=df.columns)

    return df_scale

def unnormalize(centroids):
    x = centroids[0,:]
    y = centroids[1,:]
    min_max_scale = preprocessing.MinMaxScaler()
    unscaled_x = min_max_scale.inverse_transform(x)
    unscaled_y = min_max_scale.inverse_transform(y)
    new_centroid[0,:] = unscaled_x
    new_centroid[1,:] = unscaled_y
    return new_centroid

def clustering_2D_HT(df, n_clusters=2, rseed=2):
    # First iteration of the cluster code 
    df = df[['WVHT', 'APD']]
    X = df.values
    rng = np.random.RandomState(rseed)
    i = rng.permutation(X.shape[0])[:n_clusters]
    centers = X[i]

    while True:
        labels = pairwise_distances_argmin(X, centers)

        new_centers = np.array([X[labels == j].mean(0) for j in\
                                range(n_clusters)])

        if np.all(centers == new_centers):
            break
        centers = new_centers
        
        
    plt.scatter(X[:,0], X[:,1], c=labels, s=50, cmap='viridis')
    plt.scatter(centers[:,0],centers[:,1], color='white', marker='x')
    plt.xlabel("Significant Wave Height Normalized Data")
    plt.ylabel("Average Wave Period Normalized Data")
    plt.show()
     
    
def clustering_2D_HT2(df, n_df, nc=2, t=0.001):
#    print "OG df"
#    print df
    n_df = n_df[['WVHT', 'APD']]
    X = np.array(n_df.values, dtype = float)

    km = KMeans(n_clusters= nc, init= 'random', tol=t).fit(X)
    
    label = km.labels_
    centroid = km.cluster_centers_
    print"centers"
    print centroid
#    return label
    label = np.array(label, dtype = int)
    dff = df[['WVHT', 'APD']] 
    dff.insert(loc=2,column='cluster_loc', value=label)
    
    dff_s = dff.sort_values(by ='cluster_loc')
    clust_count = np.zeros(shape =(nc,1))
#    print "clust_den", clust_den
    for index, row in dff_s.iterrows():
        for i in range(nc):
            if row['cluster_loc'] == i:
                clust_count[i] = clust_count[i] + 1
    clust_den = 100*(clust_count / len(dff_s))
    print "clust_den"
    print clust_den
    plt.scatter(X[:,0], X[:,1], c=label, s=50, cmap='viridis')  
    plt.scatter(centroid[:,0], centroid[:,1], color='white', marker = 'x')
    plt.xlabel("Significant Wave Height Normalized Data")
    plt.ylabel("Average Wave Period Normalized Data")
    plt.show()
    return dff

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(1000 * y)

    # The percent symbol needs escaping in latex
    if plt.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'


if __name__ == '__main__':

    # Calling buoying location and going through the cleaning process
    file_name = raw_input("enter buoy location: ")
    buoy_files = glob.glob(file_name + "*.txt")
    
    if str(file_name) == "HI_51202" or str(file_name) == "CA_46022":
        data = dir_cleaning(file_name, buoy_files)
    else:
        data = cleaning(file_name, buoy_files)       
        
    # 2D clustering to find relationship between Wave Period & Sig. Wave Height 
    normalized_data = normalize(data)
    
    ### Cluster Optimization ###
    
    nc = 8 #cluster numbers  ---> change into a list to iterate through
    t = 1e-20 #tolerence  ------> also need to iterate throught tolerance values, need to look at range for tolerances
    ## also need to figure out obj function for algorithm
    
    n_df = normalized_data[['WVHT', 'APD']]
    df =data
    X = np.array(n_df.values, dtype = float)

    km = KMeans(n_clusters= nc, init= 'random', tol=t).fit(X)
    
    label = km.labels_
    label_len = str(range(0,len(label)))
    centroid = km.cluster_centers_
    inertia_value = km.inertia_
#    print"centers"
#    print centroid
    print "inertia values:"
    print inertia_value

    label = np.array(label, dtype = int)
    dff = df[['WVHT', 'APD']] 
    dff.insert(loc=2,column='cluster_loc', value=label)
    dff_s = dff.sort_values(by ='cluster_loc')
    clust_count = np.zeros(shape =(nc,1))
    
    #finding representive wave heights & periods for each cluster 
    for index, row in dff_s.iterrows():
        for i in range(nc):
            if row['cluster_loc'] == i:
                clust_count[i] = clust_count[i] + 1
    
    clust_den = 100*(clust_count / len(dff_s))
    print "clust_den"
    print clust_den
    
    cluster_groups_wvht = dff.groupby('cluster_loc')['WVHT'].mean().round(2)
    print cluster_groups_wvht
    cluster_groups_apd = dff.groupby('cluster_loc')['APD'].mean().round(2)
    print cluster_groups_apd
    
#    unnorm_df = unnormalize(centroid)
#    print "un-normalized Centroids"
#    print unnorm_df
                            
    
    plt.figure()
    plt.scatter(dff[['WVHT']], dff[['APD']], c=dff[['cluster_loc']], s=50, cmap='viridis')
    plt.scatter(cluster_groups_wvht, cluster_groups_apd, color='white', marker = 'x')
    
    plt.xlabel("Significant Wave Height Normalized Data")
    plt.ylabel("Average Wave Period Normalized Data")
#    plt.legend(centroid,label_len) ##still not working.... 
    plt.show()
    

