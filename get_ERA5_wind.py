import os
import xarray as xr
import time

from download_era5_wind import *

################################# User Input ####################################

#Date
#year_inicial=input('Provide the First year of data (Years available: 1940 -2023): ')
#year_final=input('Provide the Last year of data (Years available: 1940 -2023): ')
inicial_year=1983
final_year=2021

#Grid - round values to the nearest decimal round (0.25)
#north,south,west,east=input('Provide the grid(North) of grid: ')??
north=-2
south=-50
west=32
east=102

#Project
#project=input('Provide the project name: ')
project='Maputo_Cyclones'

################################## Functions #####################################

def create_folders_downloaded(project):
    path='./Wind_Data_Downloaded_{}/'.format(project)
    if not os.path.exists(path):    
        os.makedirs(path)
    return path
    
def check_for_filecombine(path):
    file_path=path+'wind_combined.nc'
    if os.path.exists(file_path):
        os.remove(file_path)
        
################################# Main Function #################################

path=create_folders_downloaded(project)

tt1 = time.time()  
for year in range(inicial_year,final_year+1):
    ERA5_API_request(path,year,north,south,west,east)
    
print('Download Done!')

totmin = (time.time() - tt1)/60 # total time elapsed for loop over all datetimes in minutes
print('Total time for Download: %0.1f minutes' % totmin)

#Creating .nc combined
check_for_filecombine(path)
print('Creating nc combined...')
ds=xr.open_mfdataset(path+'*.nc',combine='nested',concat_dim='time',use_cftime=True)
ds.to_netcdf(path+'wind_combined.nc')

print('Nc Combined!')
print('Done!')
