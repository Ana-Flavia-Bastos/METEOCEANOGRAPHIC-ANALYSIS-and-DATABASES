import numpy as np
import pandas as pd
import warnings
from scipy.interpolate import interp2d
from mikeio.eum import EUMType, EUMUnit, ItemInfo
import metpy.calc as mpcalc
from metpy.units import units

warnings.filterwarnings('ignore')

################################# User Input ####################################

x=[32.5,32.75] #must be west/east
y=[-25.75,-26] #must be north/south

#!!!!! In the file name y comes first !!!!!!! 

p1=pd.read_csv('ERA5_-25.75_32.5_1979-2023.csv',sep=';',index_col=0, usecols=range(5)) #p1=(x1, y1)
p2=pd.read_csv('ERA5_-25.75_32.75_1979-2023.csv',sep=';',index_col=0, usecols=range(5)) #p2=(x2, y1)
p3=pd.read_csv('ERA5_-26.0_32.5_1979-2023.csv',sep=';',index_col=0, usecols=range(5)) #p3=(x1, y2)
p4=pd.read_csv('ERA5_-26.0_32.75_1979-2023.csv',sep=';',index_col=0, usecols=range(5)) #p4=(x2, y2)


#Point of Interporlation
#latitude=input('Provide the latitude for interpolation: ')
#longitude=input('Provide the longitude for interpolation: ')
latitude = -25.96
longitude = 32.55

############################## Functions of interpolation ###########################

def inter_timestep(variable,p1,p2,p3,p4,latitude,longitude):

    z_inter_l=[]
    for t in range(len(p1)):
        z=np.array([(p1.iloc[t,variable],p2.iloc[t,variable]),(p3.iloc[t,variable],p4.iloc[t,variable])])
        f=interp2d(x,y,z,kind='linear',fill_value='-1')
        z_interp=round(f(longitude,latitude)[0],3)
        z_inter_l.append(z_interp)
    z_interp_df=pd.DataFrame(z_inter_l)
    print('Done with variable...'+p1.columns.values.tolist()[variable]+'!')

    return z_interp_df

def calculate_speedNdirection_fromUV(df):

    wind_speed=[];wind_dir=[]
    for t in range(len(df)):
        u_components=df.iloc[t]['u10']
        v_components=df.iloc[t]['v10']
        speed=mpcalc.wind_speed(u_components*units('m/s'),v_components*units('m/s')).m
        dir=mpcalc.wind_direction(u_components*units('m/s'),v_components*units('m/s')).m
        wind_speed.append(speed)
        wind_dir.append(dir)
    df_speedDir=pd.DataFrame(zip(wind_speed,wind_dir))   

    return df_speedDir
    
############################## Main Function ########################

#Get time for index
start=p1.first_valid_index()
end=p1.last_valid_index()
time=pd.date_range(start=start,end=end,freq='1H')

#Interpolate all timesteps
df=pd.DataFrame()
for variable in range(len(p1.columns)):

    print('Working on variable: '+p1.columns.values.tolist()[variable])
    z_interp_df=inter_timestep(variable,p1,p2,p3,p4,latitude,longitude)
    df=pd.concat([df, z_interp_df], axis=1)

#Calculate Wind Speed and Wind Direction
print('Calculating Wind Speed and Wind Direction...')
df_speedDir=calculate_speedNdirection_fromUV(df)
df.reset_index(drop=True,inplace=True)
df_speedDir.reset_index(drop=True,inplace=True)
df=pd.concat([df, df_speedDir], axis=1)

#Organize DataFrame
df.columns=['u10','v10','Mean Sea Level Pressure','Air Temperature','Sea Surface Temperature','Wind Speed','Wind Direction']
df.index =time

items=[ItemInfo(name='u10',itemtype=EUMType.Wind_speed,unit=EUMUnit.meter_per_sec),
    ItemInfo(name='v10',itemtype=EUMType.Wind_speed,unit=EUMUnit.meter_per_sec),
    ItemInfo(name='Mean Sea Level Pressure',itemtype=EUMType.Pressure,unit=EUMUnit.hectopascal),
    ItemInfo(name='Air Temperature',itemtype=EUMType.Temperature,unit=EUMUnit.degree_Celsius),
    ItemInfo(name='Sea Surface Temperature',itemtype=EUMType.Temperature,unit=EUMUnit.degree_Celsius),
    ItemInfo(name='Wind Speed',itemtype=EUMType.Wind_speed,unit=EUMUnit.meter_per_sec),
    ItemInfo(name='Wind Direction',itemtype=EUMType.Wind_Direction,unit=EUMUnit.degree)]

#Create csv
df.to_csv("ERA5_Interp"+str(latitude)+"_"+str(longitude)+'.csv',
          sep=';',index_label='Data',columns=df.columns)
print("ERA5_csv Created !!!")

df.to_dfs0(filename="ERA5_Interp"+str(latitude)+"_"+str(longitude)+".dfs0",
            items=items, title="ERA5_Interp"+str(latitude)+"_"+str(longitude))
print("ERA5_dfs0 Created !!!")

print('Done!')