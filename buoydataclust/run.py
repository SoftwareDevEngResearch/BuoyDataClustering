# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:19:04 2020

@author: mankleh
"""


import yaml
import Check_BuoyDC
import combining_data
import cleaning
import clustering
import Cluster_visualization as cv
import Distribution_visualization as dv

if __name__ == '__main__':

    file = open("buoy_input_example.yaml", 'r')
    buoy_dict = yaml.load(file, Loader=yaml.UnsafeLoader)
    for key, value in buoy_dict.items():
        print (key + " : " + str(value))
    
    # Checking .yaml input file 
    Check_BuoyDC.check_buoy(buoy_dict)
    Check_BuoyDC.check_location(buoy_dict)
    Check_BuoyDC.check_buoy_format(buoy_dict)
    Check_BuoyDC.check_years(buoy_dict)
    Check_BuoyDC.check_cluster(buoy_dict)
    Check_BuoyDC.check_distribution(buoy_dict)
    
    # Buoy Identification name
    buoy = buoy_dict.get('Buoy','')
    years = buoy_dict.get('years','')
    
    # Combined buoy data file 
    buoy_data = combining_data.combine_files(buoy)
    
    clean_data = cleaning.cleaning(buoy,buoy_data)

    
    [Centroids, Density, cluster_data] = clustering.cluster(clean_data)
    print('')
    print("Wave Centroids")
    print(Centroids)
    print('')
    print("Density of each wave cluster")
    print(Density)
    
    
    
    S, name = dv.Bretscheider(Centroids)
   
    dv.Dist_Vis(Centroids,S,name)
    cv.cluster_vis(cluster_data,Centroids, years)