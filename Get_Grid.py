import netCDF4
import pandas as pd

################################### User Input #############################
#Subset - Lat=North/South (90 to -90) Lon=West/East (-180 to 180)
north=-10
south=-33
west=31.99
east=62.11

project='Maputo_Cyclones'
################################### Functions #############################

def read_netcdf_Data():
    fp = 'lat_lon_Waverys.nc'
    nc = netCDF4.Dataset(fp)
    lat= nc.variables['latitude'][:]
    lon= nc.variables['longitude'][:]

    return lat,lon

def creategrid(lat_subset,lon_subset):
    grid_lat=[]
    grid_lon=[]

    for i in range(len(lat_subset)): 
        for j in range(len(lon_subset)):
            grid_lat.append(lat_subset[i])
            grid_lon.append(lon_subset[j])

    df_grid=pd.DataFrame(zip(grid_lat,grid_lon)) 

    return df_grid
################################### Main Operation #############################
lat,lon=read_netcdf_Data()

lat_subset=[]
lon_subset=[]

for l in range(len(lat)):
    if lat[l]<=north and lat[l]>=south:
        lat_subset.append(round(lat[l],2))
for l in range(len(lon)):
    if lon[l]>=west and lon[l]<=east:
        lon_subset.append(round(lon[l],2))

df_grid=creategrid(lat_subset,lon_subset)
df_grid.columns=['Lat','Lon']
print(df_grid)
df_grid.to_csv('Grid_Waverys_'+project+'.csv', sep =';')

print('Done!')