import os
import xarray as xr
import time

from download_waverys_wavecomposed import *

################################# User Input ####################################

#Date
#year_inicial=input('Provide the First year of data (Years available: 1993 -2023): ')
#year_final=input('Provide the Last year of data (Years available: 1993 -2023): ')
inicial_year=2022
final_year=2022

#Grid
#north,south,west,east=input('Provide the grid(North) of grid: ')??
north=-24
south=-27
west=32
east=33.7


################################## Functions #####################################

def create_folders_downloaded():
    path='./WaveComposed_Data_Downloaded/'
    if not os.path.exists(path):    
        os.makedirs(path)
    return path
 
def check_for_filecombine(path):
    file_path=path+'wave_composed_combined.nc'
    if os.path.exists(file_path):
        os.remove(file_path)
 
################################# Main Function #################################

path=create_folders_downloaded()

tt1 = time.time()

#Download complete grid:
WAVERYS_API_request(path,inicial_year,final_year,north,south,west,east)

'''
#Download multiples points
north=pd.read_csv('Coord_download.csv',sep=';',usecols=[0]).dropna(axis=0, how='any')
south=pd.read_csv('Coord_download.csv',sep=';',usecols=[1]).dropna(axis=0, how='any')
west=pd.read_csv('Coord_download.csv',sep=';',usecols=[2]).dropna(axis=0, how='any')
east=pd.read_csv('Coord_download.csv',sep=';',usecols=[3]).dropna(axis=0, how='any')
points=[]

for lat in range(len(north)):
    for lon in range(len(west)):
        point=math.ceil(south.iloc[lat].values[0]),math.ceil(west.iloc[lon].values[0])
        WAVERYS_API_request(path,inicial_year,final_year,north.iloc[lat].values[0],south.iloc[lat].values[0],west.iloc[lon].values[0],east.iloc[lon].values[0])
        points.append(point)
with open("points_maputocyclones.txt", "w") as outfile:
    outfile.write("\n".join(str(item) for item in points))
'''

print('Download Done!')

totmin = (time.time() - tt1)/60             # total time elapsed for loop over all datetimes in minutes
print('Total time for Download: %0.1f minutes' % totmin)

#Creating .nc combined
check_for_filecombine(path)
print('Creating nc combined')
ds=xr.open_mfdataset(path+'*.nc',combine='nested',concat_dim='time',use_cftime=True)
ds.to_netcdf(path+'wave_composed_combined.nc')

print('Nc Combined!')
print('Done!')
