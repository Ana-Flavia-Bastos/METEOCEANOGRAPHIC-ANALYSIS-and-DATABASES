import netCDF4
import pandas as pd
import time
from mikeio.eum import EUMType, EUMUnit, ItemInfo

from functions_readnc_CFSR_wind import *

################################# User Input ####################################

#Date
#year_inicial=input('Provide the First year of data (Years available: 1979 - 2023-v0): ')
#year_final=input('Provide the Last year of data (Years available: 1979 - 2023-v0): ')
year_inicial=2024
year_final=2024

data_inicial=str(year_inicial)+'-01-01 00:00:00'
data_final=str(year_final)+'12-31 23:00:00'

#Lat e Lon
#latdeinteresse=input('Provide the latitude: ')
#londeinteress=input('Provide the longitude: ')
latdeinteresse=-19
londeinteresse=-39

#Version model Domain
#path_V=input('Provide the version of model domain (0,1,2 - based of resolution): ')
path_v=2

path=get_path(path_v)
print(path)

################################# Main Function #################################

#Variables
df=pd.DataFrame()

#File
tt1 = time.time()   

for year in range(int(data_inicial[0:4]),int(data_final[0:4])+1):
    for m in range(1,13):
        if m<10:
            fp='data_'+str(year)+'0'+str(m)+'.nc4'
            print('Getting info from: '+fp)
            nc = netCDF4.Dataset(path+fp)
        else:
            fp='data_'+str(year)+str(m)+'.nc4'
            print('Getting info from: '+fp)
            nc = netCDF4.Dataset(path+fp)
        
    #Read the data within file
    data_str,years=organize_data(data_inicial,data_final)

    lat,lon,times=read_netcdf_Data(nc)
    
    #Convert data to interess type
    value_lat,value_lon,dtime=convert_data(latdeinteresse,londeinteresse,times)

    #Create time list
    dtime_l=create_timelist(dtime)

    #Find index of interess for lat, lon e time
    latitude_idx,longitude_idx=findindex_forcoord(lat,value_lat,lon,value_lon)

    #Create df
    df_temp=dfseries(nc,latitude_idx,longitude_idx,dtime_l)

    df=pd.concat([df, df_temp], axis=0)

df.columns=['Data','u10','v10']

#Calculate Wind Speed and Wind Direction
print('Calculating Wind Speed and Wind Direction...')
df_speedDir=calculate_speedNdirection_fromUV(df)
df.reset_index(drop=True,inplace=True)
df_speedDir.reset_index(drop=True,inplace=True)
df=pd.concat([df, df_speedDir], axis=1)

#Organize DataFrame
df.columns=['Data','u10','v10','Wind Speed','Wind Direction']
df.set_index('Data',inplace=True)

#Get latitude e longitude de interesse
latitude=round(lat[latitude_idx],2)
longitude=round(lon[longitude_idx],2)
print(lat[:],lon[:])
print('lat= '+str(latitude),'lon= '+str(longitude))

#Create csv
df.to_csv("Wind_CFSR_"+str(latitude)+"_"+str(longitude)+"_"+str(years[0])+'-'+str(years[1])+'.csv',
          sep=';',index_label='Data',columns=df.columns)
print("Wind CFSR csv Created !!!")

items=[ItemInfo(name='u10',itemtype=EUMType.Wind_speed,unit=EUMUnit.meter_per_sec),
    ItemInfo(name='v10',itemtype=EUMType.Wind_speed,unit=EUMUnit.meter_per_sec),
    ItemInfo(name='Wind Speed',itemtype=EUMType.Wind_speed,unit=EUMUnit.meter_per_sec),
    ItemInfo(name='Wind Direction',itemtype=EUMType.Wind_Direction,unit=EUMUnit.degree)]

df.to_dfs0(filename="Wind_CFSR"+str(path_v)+"_"+str(latitude)+"_"+str(longitude)+".dfs0",
            items=items, title="Wind CFSR "+str(latitude)+"-"+str(longitude))
print("Wind CFSR dfs0 Created !!!")

totmin = (time.time() - tt1)/60             # total time elapsed for loop over all datetimes in minutes
print('Total time to read: %0.1f minutes' % totmin)