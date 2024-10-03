import netCDF4
import numpy as np
import pandas as pd
import metpy.calc as mpcalc
from metpy.units import units

def get_path(path_v):
    if int(path_v) == 0:
        path='./Wind_Data_Downloaded_CFSR/'
    elif int(path_v) == 1:
        path='./Wind_Data_Downloaded_CFSRv1/'
    elif int(path_v) == 2:
        path='./Wind_Data_Downloaded_CFSRv2/'
    return path

def organize_data(data_inicial,data_final):
    data_i=data_inicial[5:7]+'/'+data_inicial[8:10]+'/'+data_inicial[0:4]+' '+data_inicial[11:len(data_inicial)]
    data_f=data_final[5:7]+'/'+data_final[8:10]+'/'+data_final[0:4]+' '+data_final[11:len(data_final)]
    data_str=[data_i,data_f]
    years=[data_inicial[0:4],data_final[0:4]]
    return data_str,years

def read_netcdf_Data(nc):
    lat= nc.variables['latitude'][:]
    lon= nc.variables['longitude'][:]
    time=nc.variables['time']

    return lat,lon,time

def convert_data(latdeinteresse,londeinteresse,time):
    value_lat=float(latdeinteresse)
    value_lon=float(londeinteresse)
    dtime = netCDF4.num2date(time[:],time.units,only_use_cftime_datetimes=False)
    dtime=dtime.astype('datetime64')
    return value_lat,value_lon,dtime

def create_timelist(dtime):
    dtime_l=[]
    for i in range(0,len(dtime)):
        dtime_l.append(dtime[i])
    return dtime_l

def findindex_forcoord(lat,value_lat,lon,value_lon):
    latitude=find_nearest(lat,value_lat)
    longitude=find_nearest(lon,value_lon)
    return latitude,longitude

def find_nearest(array, values):
    values = np.atleast_1d(values)
    indices = np.abs(np.subtract.outer(array,values)).argmin()
    return indices

def dfseries(nc,latitude_idx,longitude_idx,dtime_l):

    df_temp=pd.DataFrame()
    u10_l=[];v10_l=[]
    
    for t in range(len(dtime_l)):
        u10_l.append(nc.variables['u-component_of_wind_height_above_ground'][t,0,latitude_idx,longitude_idx])
        v10_l.append(nc.variables['v-component_of_wind_height_above_ground'][t,0,latitude_idx,longitude_idx])

    df_temp=pd.DataFrame(zip(dtime_l,u10_l,v10_l))

    return df_temp


def calculate_speedNdirection_fromUV(df):

    wind_speed=[];wind_dir=[]
    for t in range(len(df)):
        u_components=df.iloc[t]['u10']
        v_components=df.iloc[t]['v10']
        speed=mpcalc.wind_speed(u_components*units.meter / units.second,v_components*units.meter / units.second).m
        dir=mpcalc.wind_direction(u_components*units.meter / units.second,v_components*units.meter / units.second).m
        wind_speed.append(speed)
        wind_dir.append(dir)
    df_speedDir=pd.DataFrame(zip(wind_speed,wind_dir))   

    return df_speedDir
