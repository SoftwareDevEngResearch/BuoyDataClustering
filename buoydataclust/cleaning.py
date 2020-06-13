# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 17:18:24 2020

@author: mankleh
"""

import os
import pandas as pd
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from sklearn import preprocessing


def cleaning(buoy_location,raw_data):

    current_dir = os.getcwd() #finds current working directory
    clean_data = [current_dir +'/buoyData/clean_data_' + buoy_location + '.txt']
    clean_data_name = "-".join(clean_data)

    
    try: # Opens cleaning file if it already exists in the folder location
        with open(clean_data_name, 'r') as f:
            buoy_df = pd.read_csv(clean_data_name, dtype=float)
        return buoy_df
    
    except:
        # Moving from numpy arrays for pandas dataframes (df)
        df = pd.DataFrame(data=raw_data[2:], columns=raw_data[0])
        
        df = df.loc[:, ('#YY', 'MM', 'DD', 'hh', 'mm', 'WVHT', 'APD', 'MWD')]
        df = df.rename(columns={"#YY": "YY"}, errors="raise")
        
        # Change type of dataFrame from objects to ints and floats
        df['WVHT'] = pd.to_numeric(df.WVHT,errors='coerce')
        df['APD'] = pd.to_numeric(df.APD,errors='coerce')
        df['MWD'] = pd.to_numeric(df.MWD,errors='coerce')
        df['YY'] = pd.to_numeric(df.YY,errors='coerce')
        df['MM'] = pd.to_numeric(df.MM,errors='coerce')
        df['DD'] = pd.to_numeric(df.DD,errors='coerce')
        df['hh'] = pd.to_numeric(df.hh,errors='coerce')
        df['mm'] = pd.to_numeric(df.mm,errors='coerce')

        # Check the data types of the dataframe
        # print(df.dtypes)
        # return df

#         # cleans data of any NaNa
        df = df.dropna(axis=0, how='any')
#         # Cleaning data of values of wave direction over 360 or below 0
#         # Cleaning data of wave height values over 20 m
        # count = 0

        for index, row in df.iterrows():
            if row['MWD'] > 360.0:
                df.drop(index, inplace=True)
            if row['MWD'] < 0.0:
                df.drop(index, inplace=True)

#             #     if 0.0 <= row['MWD'] <= 140.0:
#             #         # checks to see how many outliers there are 
#             #         # in the distribution
#             #         count += 1
#             # print 'below 140 degrees: ', count
#             # print ''

        df = df.reset_index(drop=True)


        for index, row in df.iterrows():
            if row['WVHT'] > 20.0:
                df.drop(index, inplace=True)


        for index, row in df.iterrows():
            if row['APD'] > 20.0:
                df.drop(index, inplace=True)

        
#         # removing outliers from the dataset 
        normalized_data = normalize(df)
        n_df = normalized_data[['WVHT', 'APD']]
        
        X = np.array(n_df.values, dtype = float)
        
        clf = LocalOutlierFactor(n_neighbors=1000, contamination=0.01)
#         # use fit_predict to compute the predicted labels of the training samples
#         # (when LOF is used for outlier detection, the estimator has no predict,
#         # decision_function and score_samples methods).
        y_pred = clf.fit_predict(X)
        df.insert(loc=8, column= 'outlier', value=y_pred)
            
        for index, row in df.iterrows():
                if row['outlier'] == -1:
                    df.drop(index, inplace=True)
        
        
        with open(clean_data_name, 'w') as f:
            df.to_csv(clean_data_name, index=False)
        return df
    
    
def normalize(df):
    x = df.values
    min_max_scale = preprocessing.MinMaxScaler()
    x_scaled = min_max_scale.fit_transform(x)
    df_scale = pd.DataFrame(x_scaled, columns=df.columns)

    return df_scale
