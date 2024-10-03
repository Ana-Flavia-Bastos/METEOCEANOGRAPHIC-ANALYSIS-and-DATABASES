import netCDF4
import pandas as pd
import math 

from functions_readnc_waverys import *

################################# User Input ####################################

#Date
#year_inicial=input('Provide the First year of data (Years available: 1993 -2023): ')
#year_final=input('Provide the Last year of data (Years available: 1993 -2023): ')
year_inicial=1993
year_final=2023

data_inicial=str(year_inicial)+'-01-01 00:00:00'
data_final=str(year_final)+'-12-31 23:00:00'
#data_final='2023-04-30 23:00:00'

#Lat e Lon
#latdeinteresse=input('Provide the latitude: ')
#londeinteress=input('Provide the longitude: ')
latdeinteresse=-2
londeinteresse=42

#Project
#project=input('Provide the project name: ')
project='Maputo'

################################# Main Function #################################

#Path
path='./WaveTotal_Data_Downloaded_{}/'.format(project)


fp='1993-2023_wavetotal_-2_100.nc'
print('Getting info from: '+fp)
nc = netCDF4.Dataset(path+fp)

#Variables names
variables_keys=list(nc.variables.keys())
variables_name=[]
for i in range(len(variables_keys)):
    if variables_keys[i] not in ['latitude','longitude','lat','lon','time']:
        variables_name.append(variables_keys[i])

    #Read the data within file
    data_str,years=organize_data(data_inicial,data_final)
    lat,lon,time=read_netcdf_Data(nc)

    #Convert data to interess type
    value_lat,value_lon,dtime=convert_data(latdeinteresse,londeinteresse,time)

    #Create time
    dtime_l=create_timelist(dtime)

    #Find index of interess for lat, lon e time
    latitude_idx,longitude_idx=findindex_forcoord(lat,value_lat,lon,value_lon)

    #Create df
    if len(variables_name) == 9:
        name=''
        df_result,items=dfseries_partionalwave(nc,latitude_idx,longitude_idx,dtime_l)
    else:
        name='WaveTotal'
        df_result,items=dfseries_totalwave(nc,latitude_idx,longitude_idx,dtime_l)

    #Get latitude e longitude de interesse
    latitude=round(lat[latitude_idx],2)
    longitude=round(lon[longitude_idx],2)
    print(lat[:],lon[:])
    print('Lat selected= '+str(latitude),'Lon selected= '+str(longitude))

    #Create csv
    df_result.to_csv("Wave_Waverys"+name+'_'+str(latitude)+"_"+str(longitude)+"_"+str(years[0])+'-'+str(years[1])+'.csv',
            sep=';',index_label='Date',columns=df_result.columns)
    print("Waverys csv Created !!!")

    df_result.to_dfs0(filename="Wave_Waverys"+name+'_'+str(latitude)+"_"+str(longitude)+"_"+str(years[0])+'-'+str(years[1])+".dfs0",
                items=items,title="Waverys"+name+'_'+str(latitude)+"_"+str(longitude)+"_"+str(years[0])+'-'+str(years[1]))
    print("Waverys dfs0 Created !!!")

print('Done!')
