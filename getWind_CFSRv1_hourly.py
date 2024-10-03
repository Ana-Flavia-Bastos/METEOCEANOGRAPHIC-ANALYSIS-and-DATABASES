
# ----------
# Get_CFSRv1
# 
# Python script to extract hourly wind data CFSR model output
# This script is used to download wind data from https://rda.ucar.edu/datasets/ds093.1/#
# Modified by Ana Flávia Bastos (anafcb95@gmail.com)
# ----------

# - - -
# INSTRUCTIONS
#
# 1) In the user input section, specify the following:
# 		- specify the list of variables to be extracted from any combination of var_list = 'surf_el,water_temp,salinity,water_u,water_v'
# 		- specify the west, east, south, and north extent of the bounding box to be extracted
#  		- specify the name of the resultDirectory where the hycom data will be saved as output
# 		- specify the date_start and number_of_days of the period to be extracted
# 2) Run this script in python or ipython
# 3) During execution you sould see the progress of each 3-hour file that is extracted during the period of interest 
#    from beginning to end. Each nc file name has the format yyyyMMdd_HH.nc to indicate the datetime stamp in UTC
#
# Occasionaly there may be times when the hycom server is not responsive 
# and the script may try several times to download a particular 3-hour time.
# Each 3-hour time is saved in a separate netcdf file in the specified output folder. 
# Sometimes if the hycom data are missing there may appear to be an endless loop of trials to download the missing data.
# In those cases it may be necessary to stop the script and change the $date_start to a value that resumes with non-missing data
# and then re-run the script with that new start time.

# - - -
# IMPORT REQUIRED PYTHON PACKAGES

import os
from datetime import *
import time
import xarray as xr
from urllib.request import urlretrieve
from urllib.error import URLError
from socket import timeout

################################# User Input ####################################

# Edit the var_list as needed to download any subset of these available variables:
#var_list = 'surf_el,water_temp,salinity,water_u,water_v'
var_list='wnd10m'

#north,south,west,east=input('Provide the grid(North) of grid: ')??
north = -19     # -80 to 80 degN          
south = -19.5   # -80 to 80 degN
west = -40    # -180 to 180 degE
east = -39.5    # -180 to 180 degE

#year_inicial=input('Provide the First year of data (Years available: 1979 - 2010): ')
#year_final=input('Provide the Last year of data (Years available: 1979 - 2010): ')
date_start = '1979-01-01 01:00:00'
date_final = '2010-01-01 00:00:00'

# - - -
# specify the directory where the extracted nc files will be saved:
ThreddsUrl = 'https://thredds.rda.ucar.edu/thredds/ncss/grid/files/g/ds093.1/'         # include the ending '/'

################################## Functions #####################################

# Check the folders created
def create_folders_downloaded():
    path='./Wind_Data_Downloaded_CFSRv1/'
    if not os.path.exists(path):    
        os.makedirs(path)
    return path

def check_for_filecombine(path):
    file_path=path+'wind_combined.nc4'
    if os.path.exists(file_path):
        os.remove(file_path)

# Correct the longitude from -180/180 to 0/360
def correct_longitude_degree(degree):
    if degree<0:
        degree_corrected = degree+359.843 # 0 to 360 degE
    elif degree==0:
        degree_corrected=degree+180
    elif degree==-180:
        degree_corrected=0
    elif degree==180:
        degree_corrected=0    
    else:   
        degree_corrected = degree 

    return degree_corrected

# Make function to extract the hycom data during the loop through all datetimes
def get_extraction(dt_i,dt_f,out_fn):
    dstr0 = dt_i.strftime('%Y-%m-%d-T%H:00:00Z')
    dstr1 = dt_f.strftime('%Y-%m-%d-T%H:00:00Z')
    year=dt_i.strftime('%Y')
    month=dt_i.strftime('%m')

    url =(ThreddsUrl+str(year)+'/wnd10m.gdas.'+str(year)+str(month)+'.grb2'+
    '?var=u-component_of_wind_height_above_ground&var=v-component_of_wind_height_above_ground'+
    '&north='+str(north)+'&west='+str(west2)+'&east='+str(east2) +'&south='+str(south)+
    '&horizStride=1&'+
    '&time_start='+dstr0+'&time_end='+dstr1+
    '&&&accept=netcdf4-classic&addLatLon=true')

   # Get the data and save as a netcdf file
    counter = 1
    got_file = False
    while (counter <= 10) and (got_file == False):
        print('  Attempting to get data, counter = ' + str(counter))
        tt0 = time.time()
        try:
            (a,b) = urlretrieve(url, out_fn)
            # a is the output file name
            # b is a message you can see with b.as_string()
        except URLError as ee:
            if hasattr(ee, 'reason'):
                print('  *We failed to reach a server.')
                print('  -Reason: ', ee.reason)
            elif hasattr(ee, 'code'):
                print('  *The server could not fulfill the request.')
                print('  -Error code: ', ee.code)
        except timeout:
            print('  *Socket timed out')
        else:
            got_file = True
            print('  Downloaded data')
        print('  Time elapsed: %0.1f seconds' % (time.time() - tt0))
        counter += 1
    if got_file:
        result = 'success'
    else:
        result = 'fail'
        
    return result

################################# Main Function #################################

# Necessary list
years=[]
dt_ilist = []
dt_flist = []

# Correct west and east for resolution 0 to 360 degE
west2=correct_longitude_degree(west)
east2=correct_longitude_degree(east)

# Correct data format
DateI = datetime.fromisoformat(date_start)
DateF= datetime.fromisoformat(date_final)

# Calculate how many years to extract from CFSR
if int(DateF.strftime('%Y'))==2010:
    nyt=(int(DateF.strftime('%Y'))+1-int(DateI.strftime('%Y')))
else:
    nyt=(int(DateF.strftime('%Y'))-int(DateI.strftime('%Y')))

for n in range(nyt):
    year=int(DateI.strftime('%Y'))+n
    years.append(year)

for i in range(len(years)):
    for m in range(1,13):
        if m<9:
            dt_i=str(years[i])+'-0'+str(m)+'-01 01:00:00'
            dt_f=str(years[i])+'-0'+str(m+1)+'-01 00:00:00'
        elif m==9:
            dt_i=str(years[i])+'-0'+str(m)+'-01 01:00:00'
            dt_f=str(years[i])+'-10-01 00:00:00'
        elif m>=10 and m<12:
            dt_i=str(years[i])+'-'+str(m)+'-01 01:00:00'
            dt_f=str(years[i])+'-'+str(m+1)+'-01 00:00:00'
        elif m==12:
            dt_i=str(years[i])+'-'+str(m)+'-01 01:00:00'
            dt_f=str(years[i]+1)+'-01-01 00:00:00'
        dt_ilist.append(datetime.fromisoformat(dt_i))
        dt_flist.append(datetime.fromisoformat(dt_f))

# Loop over all datetimes in dt_list
out_dir=create_folders_downloaded() # make sure the output directory exists, make one if not
print('\n** Working on dowload of CFSR version 1 **')
tt1 = time.time()                           # tic for total elapsed time
force_overwrite = True                      # overwrite any already existing nc files in the output folder that have the same names

for dt in range(len(dt_ilist)):
    out_fn = out_dir + datetime.strftime(dt_ilist[dt], 'data_%Y%m') + '.nc4'
    print('\n'+out_fn)
    if os.path.isfile(out_fn):
        if force_overwrite:
            os.remove(out_fn)
    if not os.path.isfile(out_fn):
        result = get_extraction(dt_ilist[dt], dt_flist[dt], out_fn)

# Total time elapsed for loop over all datetimes in minutes
totmin = (time.time() - tt1)/60

print('\nAll downloads are completed.')
print('Total time elapsed: %0.1f minutes' % totmin)

print('Done!')

# Combine all wind netcdf into one
out_dir=create_folders_downloaded()
check_for_filecombine(out_dir)
print('Creating nc combined...')
ds=xr.open_mfdataset(out_dir+'*.nc4',combine='nested',concat_dim='time',use_cftime=True)
ds.to_netcdf(out_dir+'wind_combined.nc4')

print('Nc Combined!')
print('Done!')