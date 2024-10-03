########## ERA5 MOOD ##########
INFO:
	#Site:https://www.metocean-on-demand.com/
	
	-Login needed:
		username:afb@hydroinfo.com.br
		password:H****0

##########  ERA5 Copernicus ##########
INFO:
	#Site: https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-single-levels?tab=overview

	- Update frequency: daily with a latency of about 5 days. 
	- In case that serious flaws are detected in this early release (called ERA5T),this data could be different from the final release 2 to 3 months later. 
	- In case that this occurs users are notified.

############# ERA5 functions ##########

Main to get data:
get_ERA5_wave2: Loop for year download for composed waves variables
get_ERA5_wave1: Loop for year download for total waves variables
get_ERA5_wind: Loop for year download for wind variables

To download:
dowload_era5_wave2: API request for total composed wave variables
dowload_era5_wave1: API request for total waves variables
dowload_era5_wind: API request for wind variables

To read .nc:
readnc_ERA5_wave1: Reads wavetotal.nc files and creates .csv and .dfs0 files
readnc_ERA5_wave2: Reads wavecomposed.nc files and creates .csv and .dfs0 files
readnc_ERA5_wind: Reads wind.nc files and creates .csv and .dfs0 files
functions_readnc_ERA5:Functions use in script to read .nc files

To interpolate:
interp_ERA5: Interpolate using dfs0 created with readnc

Others:
depth_ERA5: uses downloaded nc to get depth of point

############# Create ERA5 grid ##########

Get_grid_Wind: Script to create grid of interess using all model domain
*lat_lon_era5.nc = grid for all points available

Get_grid_Wave: Script to create grid of interess using all model domain
*lat_lon_era5_wave.nc = grid for all points available

########## Create dfs2 ##########
Era5nc_toDfs2 = Creates Dfs2 files for wind_combined.nc