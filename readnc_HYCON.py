import netCDF4
import pandas as pd
from mikeio.eum import EUMType, EUMUnit, ItemInfo

from functions_readnc_HYCON import *

#Input
path='./Results/'

#Project
project='MAPUTO'

#Date
data_inicial='2003-01-01 00:00:00'
data_final='2004-12-31 21:00:00'

#Lat e Long
latdeinteresse=-25.8
londeinteresse=33.2

#Depth
#Depth=0.0
depth_l=[0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 125.0, 150.0, 200.0,250.0, 300.0]


#Variables
#variables_name=['water_temp']
variables_name=['salinity']
for d in range(len(depth_l)):
    df=pd.DataFrame()
    path_depth=path+project+'/Depth_{}'.format(depth_l[d])+'/'

    #File
    for fp in range(int(data_inicial[0:4]),int(data_final[0:4])+1,1):
        
        fp='data_'+str(fp)+'.nc'
        print('Getting info from: '+fp)
        nc = netCDF4.Dataset(path_depth+fp)
        
        #Read the data within file
        data_str,years=organize_data(data_inicial,data_final)
        lat,lon,time=read_netcdf_Data(nc)

        #Convert data to interess type
        value_lat,value_lon,dtime=convert_data(latdeinteresse,londeinteresse,time)
        #print(dtime)
        #Create time list
        dtime_l=create_timelist(dtime)

        #Find index of interess for lat, lon e time
        latitude_idx,longitude_idx=findindex_forcoord(lat,value_lat,lon,value_lon)

        #Create df
        df_temp=dfseries(nc,latitude_idx,longitude_idx,dtime_l)

        df=pd.concat([df, df_temp], axis=0) 

    #df.columns=['Data','Sea Water Temperature']
    df.columns=['Data','Salinity']

    df=df.set_index('Data')

    #Get latitude e longitude de interesse
    latitude=round(lat[latitude_idx],2)
    longitude=round(lon[longitude_idx],2)

    print(lat[:],lon[:])
    print('lat= '+str(latitude),'lon= '+str(longitude))

    #Create csv
    df.to_csv(path_depth+"HYCON_"+str(latitude)+"_"+str(longitude)+"_"+str(depth_l[d])+"_"+str(years[0])+'-'+str(years[1])+'.csv',
            sep=';',index_label='Data',columns=df.columns)
    print("HYCON_csv Created !!!")

    #Create Dfs0
    #items=[ItemInfo(name='Sea Water Temperature',itemtype=EUMType.Temperature,unit=EUMUnit.degree_Celsius)]
    items=[ItemInfo(name='Salinity',itemtype=EUMType.Salinity,unit=EUMUnit.PSU)]

    df.to_dfs0(filename=path_depth+"HYCON_"+str(latitude)+"_"+str(longitude)+"_"+str(depth_l[d])+"_"+str(years[0])+'-'+str(years[1])+".dfs0",
                items=items, title="HYCON_"+str(latitude)+"_"+str(longitude))
    print("HYCON_dfs0 Created !!!")
