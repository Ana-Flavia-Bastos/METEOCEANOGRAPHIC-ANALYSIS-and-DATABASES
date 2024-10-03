import netCDF4
import pandas as pd
import time
from mikeio.eum import EUMType, EUMUnit, ItemInfo

from functions_readnc_ERA5_wave2 import *

################################# User Input ####################################

#Date
#year_inicial=input('Provide the First year of data (Years available: 1940 -2023): ')
#year_final=input('Provide the Last year of data (Years available: 1940 -2023): ')
year_inicial=2024
year_final=2024

data_inicial=str(year_inicial)+'-01-01 00:00:00'
#data_final=str(year_final)+'12-31 23:00:00'
data_final=str(year_final)+'06-28 23:00:00'
#Lat e Lon
#latdeinteresse=input('Provide the latitude: ')
#londeinteress=input('Provide the longitude: ')
latdeinteresse=-19
londeinteresse=39.5


#Project
#project=input('Provide the project name: ')
project='GALP'

################################# Main Function #################################

#Path
path='./WaveComposed_Data_Downloaded_{}/'.format(project)

#Variables
df=pd.DataFrame()

#File
tt1 = time.time()   

for fp in range(int(data_inicial[0:4]),int(data_final[0:4])+1):

    fp=str(fp)+'-'+str(fp+1)+'_wavecomposed.nc'
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

df.columns=['Data','Hm0 (Total)','Tp (Peak)','MWD','Hm0 (Swell)','Tmean (Swell)','TmFirstMoment (Swell)','TmSecondMoment (Swell)','MWD (Swell)','Hm0 (Wind)','Tmeand (Wind)','TmFirstMoment (Wind)','TmSecondMoment (Wind)','MWD (Wind)']
#df.columns=['Data','Hm0 (Total)','Tp (Peak)','MWD','Hm0 (Swell)','Hm0FirstPartition (Swell)','Hm0SecondPartition (Swell)','Tmean (Swell)','TmFirstPartition (Swell)','TmSecondPartition (Swell)','TmFirstMoment (Swell)','TmSecondMoment (Swell)','MWD (Swell)','MWDFirstPartition (Swell)','MWDSecondPartition (Swell)','Hm0 (Wind)',Tmean (Wind),'TmFirstMoment (Wind)','TmSecondMoment (Wind)','MWD (Wind)']
df.set_index('Data',inplace=True)

#Get latitude e longitude de interesse
latitude=round(lat[latitude_idx],2)
longitude=round(lon[longitude_idx],2)
print(lat[:],lon[:])
print('lat= '+str(latitude),'lon= '+str(longitude))

#Create csv
df.to_csv("Wave_Era5Composed_"+str(latitude)+"_"+str(longitude)+"_"+str(years[0])+'-'+str(years[1])+'.csv',
          sep=';',index_label='Data',columns=df.columns)
print("Wave ERA5 Composed csv Created !!!")

items=[ItemInfo(name='Hm0 (Total)',itemtype=EUMType.Wave_height,unit=EUMUnit.meter),
    ItemInfo(name='Tp (Peak)',itemtype=EUMType.Wave_period,unit=EUMUnit.second),
    ItemInfo(name='MWD',itemtype=EUMType.Wave_direction,unit=EUMUnit.degree),
    ItemInfo(name='Hm0 (Swell)',itemtype=EUMType.Wave_height,unit=EUMUnit.meter),
    #ItemInfo(name='Hm0FirstPartition (Swell)',itemtype=EUMType.Wave_height,unit=EUMUnit.meter),
    #ItemInfo(name='Hm0SecondPartition (Swell)',itemtype=EUMType.Wave_height,unit=EUMUnit.meter),
    ItemInfo(name='Tmean (Swell)',itemtype=EUMType.Wave_period,unit=EUMUnit.second),
    #ItemInfo(name='TmFirstPartition (Swell)',itemtype=EUMType.Wave_period,unit=EUMUnit.second),
    #ItemInfo(name='TmSecondPartition (Swell)',itemtype=EUMType.Wave_period,unit=EUMUnit.second),
    ItemInfo(name='TmFirstMoment (Swell)',itemtype=EUMType.Wave_period,unit=EUMUnit.second),
    ItemInfo(name='TmSecondMoment (Swell)',itemtype=EUMType.Wave_period,unit=EUMUnit.second),
    ItemInfo(name='MWD (Swell)',itemtype=EUMType.Wave_direction,unit=EUMUnit.degree),
    #ItemInfo(name='MWDFirstPartition (Swell)',itemtype=EUMType.Wave_direction,unit=EUMUnit.degree),
    #ItemInfo(name='MWDSecondPartition (Swell)',itemtype=EUMType.Wave_direction,unit=EUMUnit.degree),
    ItemInfo(name='Hm0 (Wind)',itemtype=EUMType.Wave_height,unit=EUMUnit.meter),
    ItemInfo(name='Tmean (Wind)',itemtype=EUMType.Wave_period,unit=EUMUnit.second),
    ItemInfo(name='MWD (Wind)',itemtype=EUMType.Wave_direction,unit=EUMUnit.degree)]

df.to_dfs0(filename="Wave_Era5Composed_"+str(latitude)+"_"+str(longitude)+".dfs0",
            items=items, title="ERA5 Wave Composed"+str(latitude)+"_"+str(longitude))
print("Wave ERA5 Composed dfs0 Created !!!")

totmin = (time.time() - tt1)/60             # total time elapsed for loop over all datetimes in minutes
print('Total time elapsed: %0.1f minutes' % totmin)