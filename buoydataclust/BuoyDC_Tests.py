# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:07:31 2020

@author: mankleh
"""

""" The following script is used to test the yaml checking module in the 
BuoyDataClustering suite. """


import yaml
import pytest
import Check_BuoyDC

file = open("buoy_input_example.yaml", 'r')
input_dict = yaml.load(file, Loader=yaml.UnsafeLoader)


## Testing Buoy names

buoy_fail_1 = dict(input_dict)
buoy_fail_2 = dict(input_dict)
buoy_fail_3 = dict(input_dict)

buoy_fail_1['Buoy'] = 123
buoy_fail_2['Buoy'] = '123'
buoy_fail_3['Buoy'] = ''

def test_check_buoy1():
    """ Non - String Input """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_buoy(buoy_fail_1)
    assert str(err_info.value) == 'Input file requires character input'
def test_check_buoy2():
    """ Forced string input but is integer """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_buoy(buoy_fail_2)
    assert str(err_info.value) == 'Input file requires character input'
def test_check_buoy3():
    """ Empty Input """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_buoy(buoy_fail_3)
    assert str(err_info.value) == 'Input file requires buoy name'
    
## Testing Buoy name formats
buoy_format_fail_1 = dict(input_dict)
buoy_format_fail_2 = dict(input_dict)


buoy_format_fail_1['Buoy'] = 'HI_51202'
buoy_format_fail_2['Buoy'] = 'ST_589'

    
def test_buoy_format1():
    """Incorrect buoy name format - incorrect naming convention"""
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_buoy_format(buoy_format_fail_1)
    assert str(err_info.value) == 'Input formatted incorrectly, see instructions'
    
def test_buoy_format2():
    """Incorrect buoy name format - incorrect length"""
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_buoy_format(buoy_format_fail_2)
    assert str(err_info.value) == 'Input length incorrect, see instructions'

## Testing location inputs   

location_fail_1 = dict(input_dict)
location_fail_2 = dict(input_dict)
location_fail_3 = dict(input_dict)

location_fail_1['Location'] = 123
location_fail_2['Location'] = '123'
location_fail_3['Location'] = ''

def test_check_location1():
    """ Non - String Input """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_location(location_fail_1)
    assert str(err_info.value) == 'Input file requires character input'
def test_check_location2():
    """ Forced string input but is integer """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_location(location_fail_2)
    assert str(err_info.value) == 'Input file requires character input'
def test_check_location3():
    """ Empty Input """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_location(location_fail_3)
    assert str(err_info.value) == 'Input file requires location'
    
##Testing year inputs
    
year_fail_1 = dict(input_dict)
year_fail_2 = dict(input_dict)

year_fail_1['years'] = '123'
year_fail_2['years'] = ''

def test_check_year1():
    """ Non integer Input """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_years(year_fail_1)
    assert str(err_info.value) == 'Input file requires an integer input'
def test_check_year2():
    """ Forced string input but is integer """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_years(year_fail_2)
    assert str(err_info.value) == 'Input file requires year input'
    
    
## Testing Clustering input
    
    
cluster_fail_1 = dict(input_dict)
cluster_fail_2 = dict(input_dict)
cluster_fail_3 = dict(input_dict)

cluster_fail_1['clustering'] = 12
cluster_fail_2['clustering'] = '123'
cluster_fail_3['clustering'] = ''

def test_check_cluster1():
    """ Input out of range """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_cluster(cluster_fail_1)
    assert str(err_info.value) == 'cluster type input not within range of index'
def test_check_cluster2():
    """ Non-integer input """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_cluster(cluster_fail_2)
    assert str(err_info.value) == 'Input file requires an integer input'
def test_check_cluster3():
    """ Empty Input """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_cluster(cluster_fail_3)   
    assert str(err_info.value) == 'Input file requires cluster input'
    
## Testing distribution input
    
    
distribution_fail_1 = dict(input_dict)
distribution_fail_2 = dict(input_dict)
distribution_fail_3 = dict(input_dict)

distribution_fail_1['wave_distribution'] = 12
distribution_fail_2['wave_distribution'] = '123'
distribution_fail_3['wave_distribution'] = ''

def test_check_distribution1():
    """ Input out of range """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_distribution(distribution_fail_1)
    assert str(err_info.value) == 'distribution type input not within range of index'
def test_check_distribution2():
    """ Non-integer input """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_distribution(distribution_fail_2)
    assert str(err_info.value) == 'Input file requires an integer input'
def test_check_distribution3():
    """ Empty Input """
    with pytest.raises(AssertionError) as err_info:
        Check_BuoyDC.check_distribution(distribution_fail_3)   
    assert str(err_info.value) == 'Input file requires wave distribution input'
    
    
    
    