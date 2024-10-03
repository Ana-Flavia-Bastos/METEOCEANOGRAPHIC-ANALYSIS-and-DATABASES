########## ERA5 MOOD ##########
INFO:
	#Site:https://www.metocean-on-demand.com/
	
	-Login needed:
		username:afb@hydroinfo.com.br
		password:H****0

##########  CFSR NCAR ##########
INFO:
	#Site V1: https://rda.ucar.edu/datasets/ds093.1/
	#Site V2: https://rda.ucar.edu/datasets/ds094.1/

	- Update frequency:

############# ERA5 functions ##########

Main to get data:
getWind_CFSR_hourly: Loop for 1979 - 2023 for wind variables at 0.5x0.5 resolution
getWind_CFSRv1_hourly: Loop for 1979 - 2010 for wind variables at 0.312x0.312 resolution
getWind_CFSRv2_hourly: Loop for 2012 - 2023 for wind variables at 0.205x0.204 resolution !!Not working!!


To read .nc:
readnc_CFSR_wind: Reads wind_combined.nc4 files and creates .csv and .dfs0 files
	Needs to be input of version (line 27):
		0: version complete [1979-2023]
		1: version 1 [1979 - 2010]
		2: version 2 [2012 - 2023]
functions_readnc_CFSR:Functions use in script to read .nc files

To interpolate:
interp_CFSR: Interpolate using dfs0 created with readnc

############# Create CFSR grid ##########

Get_grid_v0: Script to create grid of interess using all CFSR model domain [0.5°X0.5°]
*lat_lon_CFSR.nc = grid for all points available

Get_grid_v1: Script to create grid of interess using all CFSR V1 model domain [0.312°X0.312°]
*lat_lon_CFSRv1.nc = grid for all points available

Get_grid_v2: Script to create grid of interess using all CFSR V1 model domain [0.205°X0.204°]
*lat_lon_CFSRv2.nc = grid for all points available

########## Create dfs2 ##########
CFSRnc_toDfs2 = Creates Dfs2 files for wind_combined.nc4