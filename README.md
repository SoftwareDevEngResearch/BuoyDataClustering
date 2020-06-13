# BuoyDataClustering
 
 Version 0.1.0
 [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3893109.svg)](https://doi.org/10.5281/zenodo.3893109)
 
BuoyDataClustering is a python package used to sort, clean, and analyze historical buoy data from the National Oceanic and Atmospheric Administration's (NOAA) [National Data Buoy Center](https://www.ndbc.noaa.gov/). This packages allows the user to fill out a simple YAML text file on the buoy identification and location and then proceeds to calculate representative sea states by using [Scikit-learn K-means clustering](https://scikit-learn.org/stable/modules/clustering.html).

The current release clusters the wave data by significant wave height and significant wave period. Using the cluster location, wave spectra is found using the Bretscheider spectrum formula. An additional output of use to the user is the density or percent occurence of each sea state determined by the clustering module. 

Future releases will expand on the clustering to include wave directionality information and expand on the different types of wave spectra that can be calculated. Wave heights and periods can vary depending on the time of year, so future functionality will also include the option of calculating the sea states based on the desired season. 

## Installation

Clone the package onto your local machine. 

## Example

There is an embedded example to test BuoyDataClustering on your machine. The example uses ten years of historical data from the NOAA station 46022, which is off the coast of Northern California. An example YAML file is provided on how to set up the package with the station 46022 buoy data. To run the example:
```
python Run.py
```
Note: The Run.py file will need to be changed with user-created yaml files to run the package. 

## YAML Notes
Follow the instructions provided in YAML input file. Inputs that do not match the desired structure will be flagged. 


## Versioning
0.1.0 - initial release

## Authors

 **Hannah Mankle** - [mankleh@oregonstate.edu]

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
