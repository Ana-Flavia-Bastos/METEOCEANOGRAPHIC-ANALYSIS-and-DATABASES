import xarray as xr
import pandas as pd
import numpy as np
import mikeio
import os
from natsort import natsorted
from mikeio.eum import EUMType, EUMUnit, ItemInfo

################################# User Input ####################################

#Date
#year_inicial=input('Provide the First year of data (Years available: 1993 -2023): ')
#year_final=input('Provide the Last year of data (Years available: 1993 -2023): ')
year_inicial=1993
year_final=2023

data_inicial=str(year_inicial)+'-01-01 00:00:00'
data_final=str(year_final)+'-12-31 23:00:00'
#data_final='2023-04-30 23:00:00'

#Lat and Lon
#lat_N,lat_S,lon_W,lon_E=input('Provide the latitude an longitude range, example [2-10;32-62]: ')
lat_N=-10
lat_S=-33
lon_W=32
lon_E=62

#Espaçamento
#dx=input('Provide the distance between points: ')
dx=1

#Project
#project=input('Provide the project name: ')
project='Maputo'

################################## Functions #####################################

# Create result folder
def create_folders_results():
    path='./Boundary_dfs1_{}/'.format(project)
    if not os.path.exists(path):    
        os.makedirs(path)
    return path

#Get all files 
def getallfiles(path):

    files_N=[];files_S=[];files_E=[];files_W=[]

    for file in os.listdir(path):

        if float(file.split('_')[2])==lat_N:
            files_N.append(file)
            files_N=natsorted(files_N)

        elif float(file.split('_')[2])==lat_S:
            files_S.append(file)
            files_S=natsorted(files_S)

        elif float(file.split('_')[3].split('.')[0])==lon_E:
            files_E.append(file)

        elif float(file.split('_')[3].split('.')[0])==lon_W:
            files_W.append(file)

    files_E.append('{}_{}_{}.nc'.format(file.split('_')[0]+'_'+file.split('_')[1],lat_N,lon_E))
    files_E.append('{}_{}_{}.nc'.format(file.split('_')[0]+'_'+file.split('_')[1],lat_S,lon_E))
    files_E=natsorted(files_E)
    files_W.append('{}_{}_{}.nc'.format(file.split('_')[0]+'_'+file.split('_')[1],lat_N,lon_W))
    files_W.append('{}_{}_{}.nc'.format(file.split('_')[0]+'_'+file.split('_')[1],lat_S,lon_W))
    files_W=natsorted(files_W)

    return files_N,files_S,files_E,files_W

#Get columns of wave variables
def get_columns(df_point):

    #wave_height
    vhm0=df_point['VHM0']
    vhm0.reset_index(drop=True, inplace=True)
    #wave_period
    vtpk=df_point['VTPK']
    vtpk.reset_index(drop=True, inplace=True)
    #wave_direction
    vmdr=df_point['VMDR']
    vmdr.reset_index(drop=True, inplace=True)

    return vhm0,vtpk,vmdr

#Concatenate the dataframes into one
def get_dataframes(path,files):

    #Create time axis
    df=xr.open_dataset(path+files[0])
    times=pd.DatetimeIndex(df.time)
    cord_x=df.longitude;cord_y=df.latitude

    #Empty dataframe for wave data
    wave_height=pd.DataFrame()
    wave_period=pd.DataFrame()
    wave_direction=pd.DataFrame()

    #Create wave parameters dataframe
    for file in files:

        df_point = xr.open_dataset(path+file).to_dataframe()
        
        #Create columns from netcdf file
        vhm0,vtpk,vmdr=get_columns(df_point)

        #Concatenate the columns
        wave_height=pd.concat([wave_height,vhm0],axis=1).dropna(axis=1)
        wave_period=pd.concat([wave_period,vtpk],axis=1).dropna(axis=1)
        wave_direction=pd.concat([wave_direction,vmdr],axis=1).dropna(axis=1)

    #Create numpy array data from dataframe
    wave_height=wave_height.to_numpy()
    wave_period=wave_period.to_numpy()
    wave_direction=wave_direction.to_numpy()

    return wave_height,wave_period,wave_direction,times,cord_x,cord_y

#Calculate spreading index for each boundary
def get_spreadingIndex(wave_period):

    Tp=[10,11,12,13,14,15,16,17,18,19,20]
    nn=[4,8,10,12,16,18,20,22,26,28,30]
    function=[4,4,2,2,4,2,2,2,4,2,2]

    #Function to calculate spreading index
    if wave_period<=Tp[0]:
        spreadingIndex=4
    
    elif wave_period>[0] and wave_period<Tp[1]:
        Tp=Tp[0];nn=nn[0];function=function[1]
        spreadingIndex=(wave_period-Tp)*function+nn

    elif wave_period>[1] and wave_period<Tp[2]:
        Tp=Tp[1];nn=nn[1];function=function[2]
        spreadingIndex=(wave_period-Tp)*function+nn

    elif wave_period>[2] and wave_period<Tp[3]:
        Tp=Tp[2];nn=nn[2];function=function[3]
        spreadingIndex=(wave_period-Tp)*function+nn

    elif wave_period>[3] and wave_period<Tp[4]:
        Tp=Tp[3];nn=nn[3];function=function[4]
        spreadingIndex=(wave_period-Tp)*function+nn

    elif wave_period>[4] and wave_period<Tp[5]:
        Tp=Tp[4];nn=nn[4];function=function[5]
        spreadingIndex=(wave_period-Tp)*function+nn

    elif wave_period>[5] and wave_period<Tp[6]:
        Tp=Tp[5];nn=nn[5];function=function[6]
        spreadingIndex=(wave_period-Tp)*function+nn

    elif wave_period>[6] and wave_period<Tp[7]:
        Tp=Tp[6];nn=nn[6];function=function[7]
        spreadingIndex=(wave_period-Tp)*function+nn

    elif wave_period>[7] and wave_period<Tp[8]:
        Tp=Tp[7];nn=nn[7];function=function[8]
        spreadingIndex=(wave_period-Tp)*function+nn

    elif wave_period>[8] and wave_period<Tp[9]:
        Tp=Tp[8];nn=nn[8];function=function[9]
        spreadingIndex=(wave_period-Tp)*function+nn

    elif wave_period>[9] :
        spreadingIndex=30

    return spreadingIndex

#Create dfs1 for each boundary
def create_dfs1(path,path_result,files,dx,barreira):

    print('Creating dfs1 for boundary '+barreira+'.')
    #Calculating wave parameters of waves
    wave_height,wave_period,wave_direction,dtime_l,cord_x,cord_y=get_dataframes(path,files)

    if barreira in ['North','South']:
        geometry = mikeio.Grid1D(x0=cord_x,nx=wave_height.shape[1], dx=dx)
        #Change direction of data dfs1 oriantation !! 0 == start point of boundary!!
        if barreira == 'North':
            wave_height = np.array([sublist[::-1] for sublist in wave_height])
            wave_period = np.array([sublist[::-1] for sublist in wave_period])
            wave_direction = np.array([sublist[::-1] for sublist in wave_direction])
    else:
        geometry = mikeio.Grid1D(x0=cord_y,nx=wave_height.shape[1], dx=dx)
        #Change direction of data dfs1 oriantation !! 0 == start point of boundary!!
        if barreira == 'East': 
            wave_height = np.array([sublist[::-1] for sublist in wave_height])
            wave_period = np.array([sublist[::-1] for sublist in wave_period])
            wave_direction = np.array([sublist[::-1] for sublist in wave_direction])

    #Calculating spreading index
    spreading_index = np.array([[get_spreadingIndex(element) for element in sublist] for sublist in wave_period])

    das=[mikeio.DataArray(wave_height,
        time=dtime_l,
        geometry=geometry,
        item=mikeio.ItemInfo(name='Hm0 (Total)',itemtype=EUMType.Wave_height,unit=EUMUnit.meter)),
        mikeio.DataArray(wave_period,
        time=dtime_l,
        geometry=geometry,
        item=mikeio.ItemInfo(name='Tp (Peak)',itemtype=EUMType.Wave_period,unit=EUMUnit.second)),
        mikeio.DataArray(wave_direction,
        time=dtime_l,
        geometry=geometry,
        item=mikeio.ItemInfo(name='MWD',itemtype=EUMType.Wave_direction,unit=EUMUnit.degree)),
        mikeio.DataArray(spreading_index,
        time=dtime_l,
        geometry=geometry,
        item=mikeio.ItemInfo(name='Spreading index',itemtype=EUMType.Spreading_factor))]

    my_ds=mikeio.Dataset(das)

    # 5) Create dfs2
    my_ds.to_dfs(path_result+'Boundary_'+barreira+'.dfs1')

################################# Main Function #################################

#Path
path='./WaveTotal_Data_Downloaded_{}/'.format(project)
path_result=create_folders_results()


files_N,files_S,files_E,files_W=getallfiles(path)

for boundaries in range(4):

    if boundaries==0:
        create_dfs1(path,path_result,files_N,dx,'North')
    elif boundaries==1:
        create_dfs1(path,path_result,files_S,dx,'South')
    elif boundaries==2:
        create_dfs1(path,path_result,files_E,dx,'East')
    elif boundaries==3:
        create_dfs1(path,path_result,files_W,dx,'West')

print('Done! All boundaries created.')

