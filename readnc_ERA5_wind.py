import netCDF4
import pandas as pd
import time
from mikeio.eum import EUMType, EUMUnit, ItemInfo

from functions_readnc_ERA5_wind import *

################################# User Input ####################################

#Date
#year_inicial=input('Provide the First year of data (Years available: 1940 -2023): ')
#year_final=input('Provide the Last year of data (Years available: 1940 -2023): ')
year_inicial=1983
year_final=2083

data_inicial=str(year_inicial)+'-01-01 00:00:00'
data_final=str(year_final)+'12-31 23:00:00'

#Lat e Lon
#latdeinteresse=input('Provide the latitude: ')
#londeinteress=input('Provide the longitude: ')
latdeinteresse=-25.85
londeinteresse=32.7

#Project
#project=input('Provide the project name: ')
project='Maputo_cyclones'

################################# Main Function #################################

#Path
path='./Wind_Data_Downloaded_{}/'.format(project)

#Variables
df=pd.DataFrame()

#File
tt1 = time.time()   

for fp in range(int(data_inicial[0:4]),int(data_final[0:4])+1):

    fp=str(fp)+'-'+str(fp+1)+'_wind.nc'
    print('Getting info from: '+fp)
    nc = netCDF4.Dataset(path+fp)
    print(nc)
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

df.columns=['Data','u10','v10','Mean Sea Level Pressure','Air Temperature','Sea Surface Temperature']

#Calculate Wind Speed and Wind Direction
print('Calculating Wind Speed and Wind Direction...')
df_speedDir=calculate_speedNdirection_fromUV(df)
df.reset_index(drop=True,inplace=True)
df_speedDir.reset_index(drop=True,inplace=True)
df=pd.concat([df, df_speedDir], axis=1)

#Organize DataFrame
df.columns=['Data','u10','v10','Mean Sea Level Pressure','Air Temperature','Sea Surface Temperature','Wind Speed','Wind Direction']
df.set_index('Data',inplace=True)

#Get latitude e longitude de interesse
latitude=round(lat[latitude_idx],2)
longitude=round(lon[longitude_idx],2)
print(lat[:],lon[:])
print('lat= '+str(latitude),'lon= '+str(longitude))

#Create csv
df.to_csv("Wind_ERA5_"+str(latitude)+"_"+str(longitude)+"_"+str(years[0])+'-'+str(years[1])+'.csv',
          sep=';',index_label='Data',columns=df.columns)
print("Wind ERA5 csv Created !!!")

items=[ItemInfo(name='u10',itemtype=EUMType.Wind_speed,unit=EUMUnit.meter_per_sec),
    ItemInfo(name='v10',itemtype=EUMType.Wind_speed,unit=EUMUnit.meter_per_sec),
    ItemInfo(name='Mean Sea Level Pressure',itemtype=EUMType.Pressure,unit=EUMUnit.hectopascal),
    ItemInfo(name='Air Temperature',itemtype=EUMType.Temperature,unit=EUMUnit.degree_Celsius),
    ItemInfo(name='Sea Surface Temperature',itemtype=EUMType.Temperature,unit=EUMUnit.degree_Celsius),
    ItemInfo(name='Wind Speed',itemtype=EUMType.Wind_speed,unit=EUMUnit.meter_per_sec),
    ItemInfo(name='Wind Direction',itemtype=EUMType.Wind_Direction,unit=EUMUnit.degree)
    ]

df.to_dfs0(filename="Wind_ERA5_"+str(latitude)+"_"+str(longitude)+".dfs0",
            items=items, title="Wind ERA5 "+str(latitude)+"_"+str(longitude))
print("Wind ERA5 dfs0 Created !!!")

totmin = (time.time() - tt1)/60             # total time elapsed for loop over all datetimes in minutes
print('Total time to read: %0.1f minutes' % totmin)