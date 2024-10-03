########## Working with HYCON data ##########
#Site
https://www.hycom.org/dataserver

To download:
get_hycom_3hr: download a entire year and the depth selected into on .nc file
*In case you need multiples depth you must download each depth separate
*This function only downloads water_temp, in case you need more variables (change line 53) 

To read nc:
readnc_HYCON: uses .nc dowloaded files into dfs0
functions_readnc_HYCON: Functions use in script to read .nc files
