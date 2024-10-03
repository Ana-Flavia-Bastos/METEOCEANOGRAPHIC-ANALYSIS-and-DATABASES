import numpy as np
import pandas as pd 
import xarray as xr
import mikeio
import time
import metpy.calc as mpcalc
from metpy.units import units

#Get time 
tt1 = time.time()  

#Read nc data
folder_project_name='Wind_Data_Downloaded_Maputo_Cyclones'

ds=xr.open_dataset('./'+folder_project_name+'/wind_combined.nc')

#If nc data is to large you can subset using slice
#ds_aoi=ds.sel(longitude=slice(33,34),latitude=slice(-25.5,-26.5))
ds_aoi=ds

#Convert data to dsf2
print('Creating dfs2...')

# 1) Create time axis
times=pd.DatetimeIndex(ds.time)

# 2) Create spatial axis
g=mikeio.Grid2D(x=ds_aoi.longitude.values,y=ds_aoi.latitude.values[::-1],projection='LONG/LAT')
print(str(g))
#
# 3) Create dataset for the needed variables * If a variable needs unit conversion do it here (for example Temperature)

das=[
    mikeio.DataArray(np.flip(ds_aoi.u10.values, axis=1),
                     time=times, geometry=g,
                     item=mikeio.ItemInfo('u10',mikeio.EUMType.Wind_speed,mikeio.EUMUnit.meter_per_sec)),
    mikeio.DataArray(np.flip(ds_aoi.v10.values, axis=1),
                     time=times, geometry=g,
                     item=mikeio.ItemInfo('v10',mikeio.EUMType.Wind_speed,mikeio.EUMUnit.meter_per_sec)),
    mikeio.DataArray(np.flip(ds_aoi.msl.values, axis=1)/100,
                     time=times, geometry=g,
                     item=mikeio.ItemInfo(name='Mean Sea Level Pressure',itemtype=mikeio.EUMType.Pressure,unit=mikeio.EUMUnit.hectopascal)),                 
    mikeio.DataArray(np.flip(ds_aoi.t2m.values, axis=1)-273.15,
                     time=times, geometry=g,
                     item=mikeio.ItemInfo('Air Temperature',mikeio.EUMType.Temperature,mikeio.EUMUnit.degree_Celsius)),
    mikeio.DataArray(np.flip(ds_aoi.sst.values, axis=1)-273.15,
                     time=times, geometry=g,
                     item=mikeio.ItemInfo('Sea Surface Temperature',mikeio.EUMType.Temperature,mikeio.EUMUnit.degree_Celsius))]
# 4) Create dataset using mikeio
my_ds=mikeio.Dataset(das)

# 5) Create dfs2
my_ds.to_dfs('Era5_wind_'+str(times[0])[0:4]+'_'+str(times[-1])[0:4]+'.dfs2')

totmin = (time.time() - tt1)/60             # total time elapsed for loop over all datetimes in minutes
print('Total time to create dfs2: %0.1f minutes' % totmin)