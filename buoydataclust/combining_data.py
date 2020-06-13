# -*- coding: utf-8 -*-
"""
Created on Wed May 13 16:05:10 2020

@author: mankleh
"""
import os 
import numpy as np
import fnmatch 


def combine_files(buoy_location):
    
    current_dir = os.getcwd() #finds current working directory
    buoy_files = []
    # print(data_path)
    for filename in os.listdir(current_dir + '/buoyData/'):
        if fnmatch.fnmatch(filename, buoy_location + '*.txt'):
            buoy_files.append(current_dir +'/buoyData/' + filename)
    # print(buoy_files)
    combined_data = [current_dir +'/buoyData/combined_data_' + buoy_location + '.txt']
    combined_data_name = "-".join(combined_data)
    # print(combined_data_name)
    
    
    try: # If a combined file of the data exists, open and return the data to be analyzed
        check_file = os.stat(combined_data_name).st_size
        
        if check_file == 0:
            assert check_file, 'combined file is empty'

        else:
            with open(combined_data_name, 'r') as f:
                data = []
                for line in f:
                    data.append(line.split())
                data = np.array(data)
                # print d
                return data
    except:

        with open(combined_data_name, 'w') as outfile:
                for name in buoy_files:
                    with open(name) as infile:
                        for line in infile:
                            outfile.write(line)
                            
        with open(combined_data_name, 'r') as f:
                data = []
                for line in f:
                    data.append(line.split())
                data = np.array(data)
                # print d
                return data
                        