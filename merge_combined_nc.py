import xarray as xr
#################################################################################
"""
This code uses all wind_combined data and combines them into one. 
This combined file is then used to create a dfs2.
**The wind_combined is attained by the merger within a timerange (geet_ERA5_data).
downloaded for each grid points of get
"""
#################################################################################


#path='./Multiple_grids/'
path='./Wind_Data_Downloaded_Maputo/'

print('Combining dfs2...')

year_inicial=1993
year_final=2022

dfinal=xr.open_dataset(path+str(year_inicial)+'-'+str(year_inicial+1)+'_wind.nc')

for fp in range(year_inicial+1,year_final+1):
    d1=xr.open_dataset(path+str(fp)+'-'+str(fp+1)+'_wind.nc')
    dfinal=xr.merge([dfinal,d1])

dfinal.to_netcdf(path+'wind_combined.nc')