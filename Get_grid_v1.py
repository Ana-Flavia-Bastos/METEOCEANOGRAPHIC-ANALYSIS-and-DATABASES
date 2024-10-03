import netCDF4
import pandas as pd

################################### User Input #############################
#Subset - Lat=North/South (90 to -90) Lon=West/East (0 to 360)
north= -26
east= 48
south= -27
west= 49

hemisphere='W' #(the grid is in the east or west hemisphere)
project='Ster-Piçarras_Navegantes'
################################### Functions #############################

def read_netcdf_Data():
    fp = 'lat_lon_CFSRv1.nc4'
    nc = netCDF4.Dataset(fp)
    lat= nc.variables['latitude'][:]
    lon= nc.variables['longitude'][:]

    return lat,lon

def creategrid(lat_subset,lon_subset,hemisphere):
    grid_lat=[]
    grid_lon=[]

    for i in range(len(lat_subset)): 
        for j in range(len(lon_subset)):
            grid_lat.append(lat_subset[i])
            if hemisphere =='E':
                grid_lon.append(lon_subset[j])
            else:
                grid_lon.append(lon_subset[j]*(-1))
    df_grid=pd.DataFrame(zip(grid_lat,grid_lon)) 

    return df_grid
################################### Main Operation #############################
lat,lon=read_netcdf_Data()

lat_subset=[]
lon_subset=[]   

for l in range(len(lat)):
    if lat[l]<=north and lat[l]>=south:
        lat_subset.append(lat[l])

for l in range(len(lon)): 
    if lon[l]<=west and lon[l]>=east:
            lon_subset.append(lon[l])

print(lat_subset)
print(lon_subset)

df_grid=creategrid(lat_subset,lon_subset,hemisphere)

df_grid.columns=['Lat','Lon']
df_grid.to_csv('Grid_CFSRv1_'+project+'.csv', sep =';')