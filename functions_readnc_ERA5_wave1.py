import netCDF4
import numpy as np
import pandas as pd

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
    swl_l=[];pp1d_l=[];mwd_l=[]
    
    for t in range(len(dtime_l)):
        swl_l.append(nc.variables['swh'][t,latitude_idx,longitude_idx])
        pp1d_l.append(nc.variables['pp1d'][t,latitude_idx,longitude_idx])
        mwd_l.append(nc.variables['mwd'][t,latitude_idx,longitude_idx])


    df_temp=pd.DataFrame(zip(dtime_l,swl_l,pp1d_l,mwd_l))

    return df_temp
