import netCDF4

fp='ERA5_2022_ster_depth.nc'
nc = netCDF4.Dataset(fp)

for i in range(len(nc.variables['latitude'][:])):
    for j in range(len(nc.variables['longitude'][:])):
        print('Depth = '+str(nc.variables['wmb'][0,i,j])+'\nLatitude = '+str(nc.variables['latitude'][i])+'\nLongitude = '+str(nc.variables['longitude'][j]))