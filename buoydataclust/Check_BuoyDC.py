# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:13:42 2020

@author: mankleh
"""
""" The following script checks the buoy_input.yaml input values that inform 
all proceeding modules.

Parameters: input .yaml file

outputs: chekced buoy_dict"""

import yaml

file = open("buoy_input_example.yaml", 'r')
buoy_dict = yaml.load(file, Loader=yaml.UnsafeLoader)
# for key, value in buoy_dict.items():
#    print (key + " : " + str(value))
   
def check_buoy(buoy_dict):
        #Buoy name assertions
    buoy = buoy_dict.get('Buoy','')
    assert buoy, 'Input file requires buoy name'
    
    buoy = buoy_dict.get('Buoy')
    assert type(buoy) == str, 'Input file requires character input'
    
    try:
        int(buoy_dict.get('Buoy'))
        buoy = int(buoy_dict.get('Buoy'))
        assert type(buoy) == str, 'Input file requires character input'
        
    except ValueError:
            pass
        
def check_buoy_format(buoy_dict):
    buoy = buoy_dict.get('Buoy')
    assert 'ST_' in buoy, 'Input formatted incorrectly, see instructions'
    assert len(buoy) == 8, 'Input length incorrect, see instructions'
        
def check_location(buoy_dict):
        #Location assertions
    location = buoy_dict.get('Location','')
    assert location, 'Input file requires location'
    
    location = buoy_dict.get('Location')
    assert type(location) == str, 'Input file requires character input'
    
    try:
        int(buoy_dict.get('Location'))
        location = int(buoy_dict.get('Location'))
        assert type(location) == str, 'Input file requires character input'
        
    except ValueError:
            pass
        
def check_years(buoy_dict):
        #Years assertions
    years = buoy_dict.get('years')
    assert years, 'Input file requires year input'
    

    years = buoy_dict.get('years')
    assert type(years) == int, 'Input file requires an integer input'

def check_cluster(buoy_dict):
        #cluster assertions
    cluster = buoy_dict.get('clustering','')
    assert cluster, 'Input file requires cluster input'
    

    cluster = buoy_dict.get('clustering')
    assert type(cluster) == int, 'Input file requires an integer input'
    
    assert 1 == cluster, 'cluster type input not within range of index'

def check_distribution(buoy_dict):
        #distribution assertions
    distribution = buoy_dict.get('wave_distribution','')
    assert distribution, 'Input file requires wave distribution input'
    

    distribution = buoy_dict.get('wave_distribution')
    assert type(distribution) == int, 'Input file requires an integer input'
    
    assert 1 == distribution, 'distribution type input not within range of index'
    


# check_buoy(buoy_dict)
# check_location(buoy_dict)
# check_years(buoy_dict)
# check_cluster(buoy_dict)
# check_distribution(buoy_dict)
# check_buoy_format(buoy_dict)
   
