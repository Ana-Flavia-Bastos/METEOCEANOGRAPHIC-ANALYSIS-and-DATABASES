import numpy as np
import pandas as pd 
import xarray as xr
import mikeio
import time

#Get time 
tt1 = time.time()  

#Read nc data
ds=xr.open_dataset('wind_combined.nc4')

#If nc data is to large you can subset using slice
#ds_aoi=ds.sel(longitude=slice(33,34),latitude=slice(-25.5,-26.5))
ds_aoi=ds

#Convert data to dsf2
print('Creating dfs2...')

# 1) Create time axis
times=pd.DatetimeIndex(ds.time)

# 2) Create spatial axis
g=mikeio.Grid2D(x=ds_aoi.longitude,y=ds_aoi.latitude[::-1],projection='LONG/LAT')
print( str(g) +'Lat: '+str(ds_aoi.latitude)+'Lon:' +str(ds_aoi.longitude))
# 3) Create dataset for the needed variables * If a variable needs unit conversion do it here (for example Temperature)
das=[
    mikeio.DataArray(ds_aoi.u10.values,
                     time=times, geometry=g,
                     item=mikeio.ItemInfo('u10',mikeio.EUMType.Wind_Velocity,mikeio.EUMUnit.meter_per_sec)),
    mikeio.DataArray(np.flip(ds_aoi.v10.values,axis=1),
                     time=times, geometry=g,
                     item=mikeio.ItemInfo('v10',mikeio.EUMType.Wind_Velocity,mikeio.EUMUnit.meter_per_sec))]

# 4) Create dataset using mikeio
my_ds=mikeio.Dataset(das)

# 5) Create dfs2
my_ds.to_dfs('CFSR_wind_'+str(times[0])[0:4]+'_'+str(times[-1])[0:4]+'.dfs2')

totmin = (time.time() - tt1)/60             # total time elapsed for loop over all datetimes in minutes
print('Total time to create dfs2: %0.1f minutes' % totmin)