########## Working with WAVERYS data ##########
INFO:
	#Site: https://data.marine.copernicus.eu/product/GLOBAL_MULTIYEAR_WAV_001_032/download?dataset=cmems_mod_glo_wav_my_0.2deg_PT3H-i_202311
	
	-in case of error due credential:
*type in cmd
copernicusmarine login
set COPERNICUSMARINE_SERVICE_USERNAME=abastos2
set COPERNICUSMARINE_SERVICE_PASSWORD=Hydroinfo1234

		- Update frequency: Monthly
		- Spatial Resolution 0.2x0.2
############# Waverys functions ##########

Main to get data (for one point easier to dowload directed from website):
get_waverys_wavecomposed: Loop for year download for composed waves variables
get_waverys_wavetotal: Loop for year download for total waves variables

To download:
dowload_waverys_wavecomposed: API request for total composed wave variables
dowload_waverys_wavetotal: API request for total waves variables

To read nc:
readnc_waverys: uses .nc dowloaded files into dfs0
	- Can be used for total waves and composed waves (Swell and Wind)
functions_readnc_waverys: Functions use in script to read .nc files
readnc_waverys_todfs1: use .nc downloaded files into dfs1
	-Can create boundaries for 4 directions 
	-Change from default get_waverys and download
	-Create coord_download for project (example within folder)
Others:
depth_waverys: uses downloaded nc to get depth of point

############# Create Waverys grid ##########

Get_grid: Script to create grid of interess using all model domain
*lat_lon_Waverys.nc = grid for all points available