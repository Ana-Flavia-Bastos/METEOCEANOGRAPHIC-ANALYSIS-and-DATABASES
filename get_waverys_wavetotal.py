import os
import xarray as xr
import time
import math
import pandas as pd
from download_waverys_wavetotal import *

################################# User Input ####################################

#Date
#year_inicial=input('Provide the First year of data (Years available: 1993 -2023): ')
#year_final=input('Provide the Last year of data (Years available: 1993 -2023): ')
inicial_year=1993
final_year=2023

#Grid
#north,south,west,east=input('Provide the grid(North) of grid: ')??
north=-10
south=-33
west=32
east=62

#Project
#project=input('Provide the project name: ')
project='Maputo'
################################## Functions #####################################

def create_folders_downloaded():
    path='./WaveTotal_Data_Downloaded_{}/'.format(project)
    if not os.path.exists(path):    
        os.makedirs(path)
    return path
    
def check_for_filecombine(path):
    file_path=path+'wave_total_combined.nc'
    if os.path.exists(file_path):
        os.remove(file_path)
        
################################# Main Function #################################

path=create_folders_downloaded()

tt1 = time.time()

#Download points in grid for dfs1:
points_N=[];points_S=[]
points_W=[];points_E=[]

#Get boundary North and South
for lat in [north,south]:
    for lon in range(west,east+1,1):
        if lat == north:
            point=(lat,lon,lat+0.01,lat-0.01,lon-0.01,lon+0.01)
            #WAVERYS_API_request(path,inicial_year,final_year,lat+0.01,lat-0.01,lon-0.01,lon+0.01)
            points_N.append(point)
        else:
            point=(lat,lon,lat+0.01,lat-0.01,lon-0.01,lon+0.01)
            WAVERYS_API_request(path,inicial_year,final_year,lat+0.01,lat-0.01,lon-0.01,lon+0.01)
            points_S.append(point)

#Get boundary West and East
for lon in [west,east]:
    for lat in range(south,north+1,1):
        if lon == west:
            point=(lat,lon,lat+0.01,lat-0.01,lon-0.01,lon+0.01)
            WAVERYS_API_request(path,inicial_year,final_year,lat+0.01,lat-0.01,lon-0.01,lon+0.01)
            points_W.append(point)
        else:
            point=(lat,lon,lat+0.01,lat-0.01,lon-0.01,lon+0.01)
            WAVERYS_API_request(path,inicial_year,final_year,lat+0.01,lat-0.01,lon-0.01,lon+0.01)
            points_E.append(point)


with open("points_maputocyclones.txt", "w") as outfile:
    outfile.write('North_points\n')
    outfile.write("\n".join(str(item) for item in points_N))
    outfile.write('\nSouth_points\n')
    outfile.write("\n".join(str(item) for item in points_S))
    outfile.write('\nWest_points\n')
    outfile.write("\n".join(str(item) for item in points_W))
    outfile.write('\nEast_points\n,')
    outfile.write("\n".join(str(item) for item in points_E))

'''
#Download complete grid:
#WAVERYS_API_request(path,inicial_year,final_year,north,south,west,east)
   
print('Download Done!')
totmin = (time.time() - tt1)/60 # total time elapsed for loop over all datetimes in minutes
print('Total time for Download: %0.1f minutes' % totmin)

#Creating .nc combined
check_for_filecombine(path)
print('Creating nc combined')
ds=xr.open_mfdataset(path+'*.nc',combine='nested',concat_dim='time',use_cftime=True)
ds.to_netcdf(path+'wave_total_combined.nc')

print('Nc Combined!')
print('Done!')'''
