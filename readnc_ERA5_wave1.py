import netCDF4
import pandas as pd
import time
from mikeio.eum import EUMType, EUMUnit, ItemInfo

from functions_readnc_ERA5_wave1 import *

################################# User Input ####################################

#Date
#year_inicial=input('Provide the First year of data (Years available: 1940 -2023): ')
#year_final=input('Provide the Last year of data (Years available: 1940 -2023): ')
year_inicial=2022
year_final=2022

data_inicial=str(year_inicial)+'-01-01 00:00:00'
data_final=str(year_final)+'12-31 23:00:00'

#Lat e Lon
#latdeinteresse=input('Provide the latitude: ')
#londeinteress=input('Provide the longitude: ')
latdeinteresse=-26.5
londeinteresse=-48.5

#Path
path='./WaveTotal_Data_Downloaded/'

################################# Main Function #################################

#Variables
df=pd.DataFrame()

#File
tt1 = time.time()   

for fp in range(int(data_inicial[0:4]),int(data_final[0:4])+1):

    fp=str(fp)+'-'+str(fp+1)+'_wavetotal.nc'
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

#Organize DataFrame
df.columns=['Data','Hm0 (Total)','Tp (Peak)','MWD']
df.set_index('Data',inplace=True)

#Get latitude e longitude de interesse
latitude=round(lat[latitude_idx],2)
longitude=round(lon[longitude_idx],2)
print(lat[:],lon[:])
print('lat= '+str(latitude),'lon= '+str(longitude))

#Create csv
df.to_csv("Wave_ERA5Total_"+str(latitude)+"_"+str(longitude)+"_"+str(years[0])+'-'+str(years[1])+'.csv',
          sep=';',index_label='Data',columns=df.columns)
print("Wave ERA5 Total csv Created !!!")

items=[ItemInfo(name='Hm0 (Total)',itemtype=EUMType.Wave_height,unit=EUMUnit.meter),
    ItemInfo(name='Tp (Peak)',itemtype=EUMType.Wave_period,unit=EUMUnit.second),
    ItemInfo(name='MWD',itemtype=EUMType.Wave_direction,unit=EUMUnit.degree)]

df.to_dfs0(filename="Wave_ERA5Total_"+str(latitude)+"_"+str(longitude)+".dfs0",
            items=items, title="ERA5 Wave Total "+str(latitude)+"_"+str(longitude))
print("Wave ERA5 Total Created !!!")

totmin = (time.time() - tt1)/60             # total time elapsed for loop over all datetimes in minutes
print('Total time elapsed: %0.1f minutes' % totmin)