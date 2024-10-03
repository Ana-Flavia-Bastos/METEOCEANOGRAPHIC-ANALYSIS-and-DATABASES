import pandas as pd
import mikeio
import os
from mikeio.eum import EUMType, EUMUnit, ItemInfo

#Input
path='./Results/'

#Project
project='MAPUTO'

#Depths
depth_l=[0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0, 60.0, 70.0, 80.0, 90.0, 100.0, 125.0, 150.0, 200.0,250.0, 300.0]

#Get dfs0 list from each folder
files_l=[]
for d in range(len(depth_l)):
    for file in os.listdir(path+project+'/Depth_'+str(depth_l[d])):
        if file.endswith(".dfs0"):
            files_l.append(file)
files_l.sort(key=lambda s: int(float(s.split('_')[3]))) #sort files based on depth

#Merge all dataframe together (each column is a depth)
df_merge=pd.DataFrame()
for i in range(len(files_l)):
    ds=mikeio.read(path+project+'/Depth_'+str(depth_l[i])+'/'+files_l[i])
    ds = ds.interp_time(3600)
    df = ds.to_dataframe()
    df.columns=['Salinity-{}'.format(files_l[i]).split('_')[3]]
    df_merge=pd.concat([df_merge, df], axis=1) 

#Create data for DataAreay
data=df_merge.to_numpy()

#Get time from dataframe for DataAreay
time=df_merge.index

#time = pd.date_range(df_merge.index[0], periods=len(df_merge.index), freq="3h")

#Create Grid1 for DataAreay
geometry = mikeio.Grid1D(nx=25, dx=1)

#Create DataArray
da = mikeio.DataArray(
    data,
    time=time,
    geometry=geometry,
    item=mikeio.ItemInfo('Salinity',mikeio.EUMType.Salinity))

#Create dfs1 from DataArray
da.to_dfs(path+project+'/'+'Salinity.dfs1')