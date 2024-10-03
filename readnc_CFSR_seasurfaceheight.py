import netCDF4
import pandas as pd
import time
from mikeio.eum import EUMType, EUMUnit, ItemInfo

from functions_readnc_CFSR_seasurfaceheight import *

################################# User Input ####################################

#Date
#year_inicial=input('Provide the First year of data (Years available: 1979 - 2023-v0): ')
#year_final=input('Provide the Last year of data (Years available: 1979 - 2023-v0): ')
year_inicial=2024
year_final=2024

#data_inicial=str(year_inicial)+'-01-01 00:00:00'
#data_final=str(year_final)+'12-31 23:00:00'
data_inicial=str(year_inicial)+'-05-01 00:00:00'
data_final=str(year_final)+'07-01 00:00:00'

#Lat e Lon  
# Subset - Lat=North/South (90 to -90) Lon=West/East (0 to 360)
#latdeinteresse=input('Provide the latitude: ')
#londeinteress=input('Provide the longitude: ')
latdeinteresse=-19.25
londeinteresse=320.75

#Path
path='./'

#Project
#project=input('Provide the project name: ')
project='GALP'
################################# Main Function #################################
fp=['ocnslh.cdas1.202405.grb2.nc4','ocnslh.cdas1.202406.grb2.nc4']
#Variables
df=pd.DataFrame()

#File
tt1 = time.time()   

#for year in range(int(data_inicial[0:4]),int(data_final[0:4])+1):
for f in fp:
    fp=f
    nc = netCDF4.Dataset(path+fp)
    print(nc)
    #Read the data within file
    data_str,years=organize_data(data_inicial,data_final)

    lat,lon,times=read_netcdf_Data(nc)
    print(lat)
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
df.columns=['Data','Water Level']
df.set_index('Data',inplace=True)

#Get latitude e longitude de interesse
latitude=round(lat[latitude_idx],2)
longitude=round(lon[longitude_idx],2)
print(lat[:],lon[:])
print('lat= '+str(latitude),'lon= '+str(longitude))

#Create csv
df.to_csv("WaterLevel_CFSR_"+str(latitude)+"_"+str(longitude)+"_"+str(years[0])+'-'+str(years[1])+'.csv',
          sep=';',index_label='Data',columns=df.columns)
print("Water Level CFSR csv Created !!!")

items=[ItemInfo(name='Water Level',itemtype=EUMType.Water_Level,unit=EUMUnit.meter),
]

df.to_dfs0(filename="Water Level_CFSR_"+str(latitude)+"_"+str(longitude)+".dfs0",
            items=items, title="Water Level CFSR "+str(latitude)+"-"+str(longitude))
print("Water Level CFSR dfs0 Created !!!")

totmin = (time.time() - tt1)/60             # total time elapsed for loop over all datetimes in minutes
print('Total time to read: %0.1f minutes' % totmin)