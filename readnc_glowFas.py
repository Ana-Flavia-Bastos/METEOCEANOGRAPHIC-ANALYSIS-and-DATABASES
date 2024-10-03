import netCDF4
import pandas as pd
from mikeio.eum import EUMType, EUMUnit, ItemInfo

from functions_readnc_glowFas import *

################################# User Input ####################################

#Input
df=pd.DataFrame()

#Date
data_inicial='2021-01-01 00:00:00'
data_final='2021-06-01 00:00:00'

latdeinteresse=-14.95
londeinteresse=-51.15

################################# Main Function #################################

for fp in range(int(data_inicial[5:7]),int(data_final[5:7])+1,5):

    if fp<10:
        fp='date_'+data_inicial[0:5]+'0'+str(fp)+'.nc'
    else:
        fp='date_'+data_inicial[0:5]+str(fp)+'.nc'
    #fp='date.nc'
    nc = netCDF4.Dataset(fp)

    #Read the data within file
    data_str,years=organize_data(data_inicial,data_final)
    lat,lon,time=read_netcdf_Data(nc)

    #Convert data to interess type
    if londeinteresse<0:
        londeinteresse=360+londeinteresse

    value_lat,value_lon,dtime=convert_data(latdeinteresse,londeinteresse,time)

    #Create time list
    dtime_l=create_timelist(dtime)

    #Find index of interess for lat, lon e time
    latitude_idx,longitude_idx=findindex_forcoord(lat,value_lat,lon,value_lon)

    #Create df
    df_temp=dfseries(nc,latitude_idx,longitude_idx,dtime_l)

    df=pd.concat([df, df_temp], axis=0)

#Rename df
df.columns=['Data','Discharge 24H']
df=df.set_index('Data')

#Get latitude e longitude de interesse
latitude=round(lat[latitude_idx],3)
longitude=round(lon[longitude_idx],3)
print('latitudes',lat[:],'longitudes',lon[:],sep='\n')
print('lat= '+str(latitude),'lon= '+str(longitude))

#Create csv

df.to_csv("Discharge24H"+str(latitude)+"_"+str(longitude)+"_"+str(years[0])+'-'+str(years[1])+'.csv',
        sep=';',index_label='Data',columns=df.columns)
print("Discharge24H_csv Created !!!")

items=[ItemInfo(name='Discharge 24H',itemtype=EUMType.Discharge,unit=EUMUnit.meter_pow_3_per_sec)]

df.to_dfs0(filename="Discharge24H_"+str(latitude)+"_"+str(longitude)+".dfs0",
            items=items, title="Discharge24H_"+str(latitude)+"_"+str(longitude))
print("Discharge24H_dfs0 Created !!!")

print('Done')

