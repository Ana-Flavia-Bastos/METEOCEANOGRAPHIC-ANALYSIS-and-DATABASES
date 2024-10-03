import netCDF4

fp='cmems_mod_glo_wav_my_0.2deg_static_1719325193565.nc'
nc = netCDF4.Dataset(fp)

for i in range(len(nc.variables['latitude'][:])):
    for j in range(len(nc.variables['longitude'][:])):
        print('Depth = '+str(nc.variables['deptho'][i,j])+'\nLatitude = '+str(nc.variables['latitude'][i])+'\nLongitude = '+str(nc.variables['longitude'][j]))