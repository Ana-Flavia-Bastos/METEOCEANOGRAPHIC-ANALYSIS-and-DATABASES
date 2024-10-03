
# ----------
# get_hycom_3hr.py 
# 
# Python script to extract 3-hr hycom model output
# This script is used to download hycom hindcast data from www.hycom.org 

# Adapted from a LiveOcean script by Parker MacCready (https://github.com/parkermac/LiveOcean)
# Modified by Greg Pelletier (gjpelletier@gmail.com) for standalone use (https://github.com/gjpelletier/get_hycom)
# Modified by Ana Flávia Bastos (anafcb95@gmail.com) for standalone use [03/04/2024]
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

# - - -
# IMPORT REQUIRED PYTHON PACKAGES

import os
from datetime import *
import time
from urllib.request import urlretrieve
from urllib.error import URLError
from socket import timeout

################################# User Input ####################################

# Edit the var_list as needed to download any subset of these available variables:
#var_list = 'surf_el,water_temp,salinity,water_u,water_v'
var_list='salinity'

#north,south,west,east=input('Provide the grid(North) of grid: ')??
north = -25     # -80 to 80 degN          
south = -26   # -80 to 80 degN
west = 33    # -180 to 180 degE
east = 33.4    # -180 to 180 degE

#Project
project='MAPUTO'

# specify vertical limits (Depths must be:  0.0 2.0 4.0 6.0 8.0 10.0 12.0 15.0 20.0 25.0 30.0 35.0 40.0 45.0 50.0 60.0 70.0 80.0 90.0 100.0 125.0 150.0 200.0 250.0 300.0 350.0 400.0 500.0 600.0 700.0 800.0 900.0 1000.0 1250.0 1500.0 2000.0 2500.0 3000.0 4000.0 5000.0 m)
#depth=input('Provide the depth: ')
#depth_l=[ 0.0 2.0 4.0 6.0 8.0 10.0 12.0 15.0 20.0 25.0 30.0 35.0 40.0 45.0 50.0 60.0 70.0 80.0 90.0 100.0 125.0 150.0 200.0 250.0 300.0]
depth_l=[150.0]

#Time
#year_inicial=input('Provide the First year of data (Years available: 1994 - 2015): ')
#year_final=input('Provide the Last year of data (Years available: 1994 - 2015): ')
date_start = '2003-01-01 00:00:00'      # ISO formatted (YYYY-MM-DD) string for the starting datetime for the data to be downloaded (starting hour must be either 00, 03, 06, 09, 12, 15, 18, or 21, and must be 12 if the date_start is Jan 1 of the year or first day of the expt. The date_start must be within the range of dates for the glb and expt as described at www.hycom.org)
date_final = '2004-12-31 21:00:00'

# Specify the glb, expt, date_start, and number_of_days up to one year at a time between 1994 to present
glb = 'GLBv0.08'                        # code for the HYCOM grid that was used to produce the data to be downloaded as described at www.hycom.org
expt = '53.X'                           # code for the HYCOM experiment that was used to generate the data to be downloaded as described at www.hycom.org

# IMPORTANT: Note for selecting the correct glb and expt for the dates to be downloaded (more info on the glb and expt is available at www.hycom.org if needed):
# Use glb = 'GLBv0.08' and expt = '53.X' for dates between 1994-2015
# Use glb = 'GLBv0.08' and expt = '56.3' for dates between 1/1/2016 or 7/1/2014 to 4/30/2016
# Use glb = 'GLBv0.08' and expt = '57.2' for dates between 5/1/2016 to 1/31/2017
# Use glb = 'GLBv0.08' and expt = '92.8' for dates between 2/1/2017 to 5/31/2017
# Use glb = 'GLBv0.08' and expt = '57.7' for dates between 6/1/2017 to 9/30/2017
# Use glb = 'GLBv0.08' and expt = '92.9' for dates between 10/1/2017 to 12/31/2017
# Use glb = 'GLBv0.08' and expt = '93.0' for dates between 1/1/2018 to 12/31/2018 or 2/18/2020
# Use glb = 'GLBy0.08' and expt = '93.0' for dates between 12/4/2018 or 1/1/2019-present

################################## Functions #####################################

# make function to create a directory if it does not already exist
def ensure_dir(file_path):
    # create a folder if it does not already exist
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def correct_longitude_degree(degree):
    if degree<0:
        degree_corrected = degree+360 # 0 to 360 degE
    elif degree==0:
        degree_corrected=degree+180
    elif degree==-180:
        degree_corrected=0
    elif degree==180:
        degree_corrected=360    
    else:   
        degree_corrected = degree 

    return degree_corrected

# make function to extract the hycom data during the loop through all datetimes
def get_extraction(dt_i,dt_f, out_fn, var_list,depth):
    dstr0 = dt_i.strftime('%Y-%m-%d-T%H:00:00Z')
    dstr1 = dt_f.strftime('%Y-%m-%d-T%H:00:00Z')
    dstr0_ajusted=str(dstr0).replace(':','%3A')
    dstr1_ajusted=str(dstr1).replace(':','%3A')
    if expt == '53.X'or'56.3'or'57.2'or'57.7':
        url = ('http://ncss.hycom.org/thredds/ncss/' + glb + '/expt_' + expt + '/data/' + dt_f.strftime('%Y') + 
            '?var='+var_list +
            '&north='+str(north)+'&west='+str(west)+'&east='+str(east) +'&south='+str(south)+
            '&disableProjSubset=on&horizStride=1' +
            '&time_start='+dstr0_ajusted+'&time_end='+dstr1_ajusted+'&timeStride=1' +
            '&vertCoord='+str(depth)+
            '&addLatLon=true&accept=netcdf')
    else:
        url = ('http://ncss.hycom.org/thredds/ncss/' + glb + '/expt_' + expt + 
            '?var='+var_list +
            '&north='+str(north)+'&west='+str(west2)+'&east='+str(east2) +'&south='+str(south)+
            '&disableProjSubset=on&horizStride=1' +
            '&time_start='+dstr0_ajusted+'&time_end='+dstr1_ajusted+'&timeStride=1' +
            '&vertCoord='+str(depth)+
            '&addLatLon=true&accept=netcdf')
    # get the data and save as a netcdf file
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

#Necessary list
years=[]
dt_ilist = []
dt_flist = []

#Get west and east for resolution 0 to 360 degE for different expt
if expt not in ['53.X','56.3','57.2','57.7']:
    west2=correct_longitude_degree(west)
    east2=correct_longitude_degree(east)

# Correct data format
YearS = datetime.fromisoformat(date_start)
YearF= datetime.fromisoformat(date_final)

#Calculate how many years to extract from hycon
nyt=(int(YearF.strftime('%Y'))-int(YearS.strftime('%Y')))+1

for n in range(nyt):
    year=int(YearS.strftime('%Y'))+n
    years.append(year)

for i in range(len(years)):
    if years[i] == 1994:
        dt_i=str(years[i])+'-01-01 12:00:00'
        dt_f=str(years[i])+'-12-31 21:00:00'
    elif years[i] == 2015:
        dt_i=str(years[i])+'-01-01 00:00:00'
        dt_f= str(years[i])+'-12-31 09:00:00'       
    elif years[-1] == years[-1]:
        dt_i=str(years[i])+'-01-01 00:00:00'
        dt_f=str(years[i])+'-12-31 21:00:00'
    else:  
        dt_i=str(years[i])+'-01-01 00:00:00'
        dt_f=str(years[i+1])+'-12-31 21:00:00'
    dt_ilist.append(datetime.fromisoformat(dt_i))
    dt_flist.append(datetime.fromisoformat(dt_f))

# - - -
# loop over all datetimes in dt_list
for d in range(len(depth_l)):
    out_dir = 'Results/'+project+'/Depth_'+str(depth_l[d])+'/'   # specify output directory adding the ending '/'
    ensure_dir(out_dir)                         # make sure the output directory exists, make one if not

    print('\n** Working on ' + glb + '/expt_' + expt + ' **')

    tt1 = time.time()                           # tic for total elapsed time
    force_overwrite = True                      # overwrite any already existing nc files in the output folder that have the same names

    for dt in range(len(dt_ilist)):
        out_fn = out_dir + datetime.strftime(dt_flist[dt], 'data_%Y') + '.nc'
        print(out_fn)
        if os.path.isfile(out_fn):
            if force_overwrite:
                os.remove(out_fn)
        if not os.path.isfile(out_fn):
            result = get_extraction(dt_ilist[dt], dt_flist[dt], out_fn, var_list,depth_l[d])

# final message
totmin = (time.time() - tt1)/60             # total time elapsed for loop over all datetimes in minutes

print('\nAll downloads are completed.')
print('Total time elapsed: %0.1f minutes' % totmin)

print('Done!')
