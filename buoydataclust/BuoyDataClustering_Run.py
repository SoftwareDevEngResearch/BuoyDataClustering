# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:19:04 2020

@author: mankleh
"""


import yaml
import Check_BuoyDC
import glob
import os

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
    
    buoy = buoy_dict.get('Buoy','')
    
    cur_dir = os.getcwd() 
    buoy_files = glob.glob("/buoyData" + buoy + "*.txt")