# -*- coding: utf-8 -*-
"""
Created on Wed May 13 12:28:04 2020

@author: mankleh
"""


## This module serves as the input file to analyze NOAA Buoy data ##
## The user will receive cluster information on the Buoy site inputted and 
## desired wave distribution information and visualization 

class buoy_information:
    def __init__(self, buoy_location, yrs):
        self.buoy_location = buoy_location 
        self.yrs = yrs 


def welcome() :
    version = 'alpha v 0.0.1'
    print("Welcome to BuoyDataClustering, this package analyses NOAA buoy data and finds wave conditions with k-means clustering.")
    print('')
    print("The current version is ", version)
    print('')
    print("BuoyDataCLustering requires Python 3.7+")
    print('')
    
def intro_question():
    ## Questions to establish the buoy data being analyzed ##
    fail_count = 0 
    intro_1 = input("Do you have NOAA buoy data you would like to analyze? (yes or no): ")
    if intro_1 != 'yes' and intro_1 != 'no':
        while intro_1 != 'yes' and intro_1 != 'no':
            print('')
            fail_count = fail_count + 1
            
            if fail_count >= 3:
                print("Three failed attempts, re-run the package and visit the documentation.")
                intro_1 = 'failed'
                return intro_1
            else:
                print('')
                print("Incorrect input, please answer yes or no.")
                intro_1 = input("Do you have NOAA buoy data you would like to analyze? (yes or no): ")
        fail_count = 0
        return intro_1
    else:
        fail_count = 0
        return intro_1
        
        
def buoy_questions():
    ## Asks user about the buoy identifier and the number of years of buoy data that will be analyzed ##
    buoy_location= []
    yrs = []
    # clustering = []
    # distribution = []
    
    intro_1 = intro_question()
    
    if intro_1 == 'failed':
        return intro_1
    elif intro_1 == 'no':
        print("This package only supports inputting NOAA buoy .txt files")
        return intro_1
    elif intro_1 == 'yes':
        print('')
        print("Please enter a buoy location in the following format:")
        print("state appreviation_buoy number")
        print("example: HI_51202")
        buoy_location = input("Enter Buoy Location: ")
        print('')
        yrs = input("How many years of data will you be including? : ")
        print('')
        
    while len(buoy_location) == 0 or len(yrs) == 0:
        
        if len(buoy_location) == 0:
            fail_count = 0
            while len(buoy_location) == 0:
                fail_count = fail_count + 1
                if fail_count == 3:
                    buoy_location = 'failed location'
                    print("Three failed attempts, re-run the package and visit the documentation.")
                    return buoy_location 
                else:
                    print("invalid buoy location.")
                    print('')
                    buoy_location = input("please enter buoy location : ")
        elif len(yrs) == 0:
            fail_count = 0
            while len(yrs) == 0:
                fail_count = fail_count + 1
                if fail_count == 3:
                    yrs = 'failed'
                    print("Three failed attempts, re-run the package and visit the documentation.")
                    return yrs
                else:
                    print("invalid number of years.")
                    print('')
                    yrs = input("please enter how many years of buoy data you will be using : ")
   
    while len(buoy_location) != 8:
        fail_count = 0
        while len(buoy_location) != 8:
            fail_count = fail_count + 1
            if fail_count == 3:    
                buoy_location = 'failed locaiton'
                print("Three failed attempts, re-run the package and visit the documentation.")
                return buoy_location
            else:
                print("invalid buoy location.")
                print('')
                buoy_location = input("please enter correct buoy location convention : ")
                
    while len(yrs) >= 3:
        fail_count = 0
        while len(yrs) >= 3:
            fail_count = fail_count + 1
            if fail_count == 3:
                yrs = 'failed'
                print("Three failed attempts, re-run the package and visit the documentation.")
                return yrs
            else:
                print("invalid number of years, must be less than 100")
                print('')
                yrs = input("please enter how many years of buoy data you will be using : ")
    return buoy_information(buoy_location, yrs)

def output_requirements():
    ## establishes how the data will be clustered and the output wave distributions##
    clustering = []
    wave_distribution = []
    
    cluster_options = ['wave height and wave period',
                       'wave height and directionality',
                       'wave period and directionality',
                       '3D clustering (WVHT,WPD,Dir)']
    
    distribution_options = ['bretschneider','JONSWAP','Rayleigh']
    
    print('\n'.join('{}: {}'.format(*k) for k in enumerate(cluster_options))) 
    
    success = False
    trys = 0
    while success == False:
        try:
            clustering = int(input('Using the clustering options above, what option would you like to use?'))
            if clustering > 3 or clustering < 0:
                if trys >= 2:
                    print('Number of attempts reached. Please rerun the package and visit the documentation.')
                    return 'fail'
                else:
                    print('Number inputed not found on supplied list. Try again...')
                    trys = trys + 1 
            else:
                success = True
                
        except ValueError:
            print( 'That was not a valid number.  Try again...')
            
    print('\n'.join('{}: {}'.format(*k) for k in enumerate(distribution_options))) 
            
    success = False 
    trys = 0 
    while success == False:
        try:
            wave_distribution = int(input('Using the wave distribution options above, what distribution would you like to use?'))
            if wave_distribution > 2 or wave_distribution < 0:
                if trys >= 2:
                    print('Number of attempts reached. Please rerun the package and visit the documentation.')
                    return 'fail'
                else:
                    print('Number inputed not found on supplied list. Try again...')
                    trys = trys + 1 
            else:
                success = True
        except ValueError:
            print( 'That was not a valid number.  Try again...')
            
    return clustering, wave_distribution