# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 19:41:43 2020

@author: mankleh
"""


import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import preprocessing


def cluster(buoy_data):
    
    normalized_data = normalize(buoy_data)
    
    nc = 8 #cluster numbers  ---> change into a list to iterate through
    t = 1e-20 #tolerence  ------> also need to iterate throught tolerance values, need to look at range for tolerances
    ## also need to figure out obj function for algorithm
    
    n_df = normalized_data[['WVHT', 'APD']]
    X = np.array(n_df.values, dtype = float)

    km = KMeans(n_clusters= nc, init= 'random', tol=t).fit(X)
    
    label = km.labels_
    # label_len = str(range(0,len(label)))
    # centroid = km.cluster_centers_
    # inertia_value = km.inertia_


    label = np.array(label, dtype = int)
    df = buoy_data[['WVHT', 'APD']] 
    df.insert(loc=2,column='cluster_loc', value=label)
    df_sorted = df.sort_values(by ='cluster_loc')
    cluster_count = np.zeros(shape =(nc,1))
    
    #finding representive wave heights & periods for each cluster 
    for index, row in df_sorted.iterrows():
        for i in range(nc):
            if row['cluster_loc'] == i:
                cluster_count[i] = cluster_count[i] + 1
    
    Density = 100*(cluster_count / len(df_sorted))
    
    cluster_groups_wvht = df.groupby('cluster_loc')['WVHT'].mean().round(2)
    cluster_groups_apd = df.groupby('cluster_loc')['APD'].mean().round(2)

    
    Centroids = np.array([cluster_groups_wvht.values, cluster_groups_apd.values])
    return Centroids, Density, df
    
def normalize(df):
    x = df.values
    min_max_scale = preprocessing.MinMaxScaler()
    x_scaled = min_max_scale.fit_transform(x)
    df_scale = pd.DataFrame(x_scaled, columns=df.columns)

    return df_scale