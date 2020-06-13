# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 21:59:04 2020

@author: mankleh
"""

import matplotlib.pyplot as plt
import numpy as np

def cluster_vis(cluster_data,centroids, years):
    dff = cluster_data
    loc = np.array(dff[['cluster_loc']])

    
    plt.figure()
    plt.scatter(dff[['WVHT']], dff[['APD']], c=loc, s=50, cmap='viridis')
    plt.scatter(centroids[0,:], centroids[1,:], color='black', marker = 'x')
    plt.title('Significant wave height and wave period clusters for '+str(years)+' years')
    plt.xlabel("Significant Wave Height [m]")
    plt.ylabel("Average Wave Period [Sec]")
    plt.show()
