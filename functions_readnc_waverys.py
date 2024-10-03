import netCDF4
import numpy as np
import pandas as pd
from mikeio.eum import EUMType, EUMUnit, ItemInfo

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

def dfseries_partionalwave(nc,latitude_idx,longitude_idx,dtime_l):

    df_wave=pd.DataFrame()
    
    #Organize all variables
    VHM0_l=[];VTPK_l=[];VMDR_l=[]
    VHM0_SW1_l=[];VTM01_SW1_l=[];VMDR_SW1_l=[]
    VHM0_WW_l=[];VTM01_WW_l=[];VDMR_WW_l=[]
    
    for t in range(len(dtime_l)):
        VHM0_l.append(nc.variables['VHM0'][t,latitude_idx,longitude_idx])
        VTPK_l.append(nc.variables['VTPK'][t,latitude_idx,longitude_idx])
        VMDR_l.append(nc.variables['VMDR'][t,latitude_idx,longitude_idx])
        VHM0_SW1_l.append(nc.variables['VHM0_SW1'][t,latitude_idx,longitude_idx])
        VTM01_SW1_l.append(nc.variables['VTM01_SW1'][t,latitude_idx,longitude_idx])
        VMDR_SW1_l.append(nc.variables['VMDR_SW1'][t,latitude_idx,longitude_idx])
        VHM0_WW_l.append(nc.variables['VHM0_WW'][t,latitude_idx,longitude_idx])
        VTM01_WW_l.append(nc.variables['VTM01_WW'][t,latitude_idx,longitude_idx])
        VDMR_WW_l.append(nc.variables['VMDR_WW'][t,latitude_idx,longitude_idx])

    df_wave=pd.DataFrame(zip(dtime_l,VHM0_l,VTPK_l,VMDR_l,VHM0_SW1_l,VTM01_SW1_l,VMDR_SW1_l,VHM0_WW_l,VTM01_WW_l,VDMR_WW_l))

    #Create items for dfs0
    items=[ItemInfo(name='Hm0 (Total)',itemtype=EUMType.Wave_height,unit=EUMUnit.meter),
        ItemInfo(name='Tp (Peak)',itemtype=EUMType.Wave_period,unit=EUMUnit.second),
        ItemInfo(name='MWD',itemtype=EUMType.Wave_direction,unit=EUMUnit.degree),
        ItemInfo(name='Hm0 (Swell)',itemtype=EUMType.Wave_height,unit=EUMUnit.meter),
        ItemInfo(name='Tp (Swell)',itemtype=EUMType.Wave_period,unit=EUMUnit.second),
        ItemInfo(name='MWD (Swell)',itemtype=EUMType.Wave_direction,unit=EUMUnit.degree),
        ItemInfo(name='Hm0 (Wind)',itemtype=EUMType.Wave_height,unit=EUMUnit.meter),
        ItemInfo(name='Tp (Wind)',itemtype=EUMType.Wave_period,unit=EUMUnit.second),
        ItemInfo(name='MWD (Wind)',itemtype=EUMType.Wave_direction,unit=EUMUnit.degree)]

    # Organize dataframe
    df_wave.columns=['Date','Hm0 (Total)','Tp (Peak)','MWD','Hm0 (Swell)','Tp (Swell)','MWD (Swell)','Hm0 (Wind)','Tp (Wind)','MWD (Wind)']
    df_wave.set_index('Date',inplace=True)
    
    return df_wave,items

def dfseries_totalwave(nc,latitude_idx,longitude_idx,dtime_l):

    df_total=pd.DataFrame()
    
    #Organize all variables
    VHM0_l=[];VTPK_l=[];VMDR_l=[]
    
    for t in range(len(dtime_l)):
        VHM0_l.append(nc.variables['VHM0'][t,latitude_idx,longitude_idx])
        VTPK_l.append(nc.variables['VTPK'][t,latitude_idx,longitude_idx])
        VMDR_l.append(nc.variables['VMDR'][t,latitude_idx,longitude_idx])

    df_total=pd.DataFrame(zip(dtime_l,VHM0_l,VTPK_l,VMDR_l))

    #Create items for dfs0
    items=[ItemInfo(name='Hm0 (Total)',itemtype=EUMType.Wave_height,unit=EUMUnit.meter),
        ItemInfo(name='Tp (Peak)',itemtype=EUMType.Wave_period,unit=EUMUnit.second),
        ItemInfo(name='MWD',itemtype=EUMType.Wave_direction,unit=EUMUnit.degree)]
    
    # Organize dataframe
    df_total.columns=['Date','Hm0 (Total)','Tp','MWD']
    df_total.set_index('Date',inplace=True)

    return df_total,items