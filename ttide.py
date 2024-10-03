import ttide as tt
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

################################# User Input ####################################
#Read Excel with Datetime and Elevation with header
#file=input(('Provide the file with tide elevations: ')
#outfile=input(('Provide the name for output file: ')
df=pd.read_excel('Tide_Maputo.xlsx',header=0)

#Grid
#lat=input(('Provide the latitude of station (degree): ')
lat=-25.96

#Timestep
#lat=input(('Provide the timestep between measurements of station (degree): ')
timestep=1

################################# Main Function #################################

#Get Datetime
t = df.iloc[:,0]
t=pd.to_datetime(t)

#Get tide elevation
elev = df.iloc[:,1]
elev=elev.to_numpy()

#constituents Analysis
tfit_e = tt.t_tide(elev,dt=timestep,stime=t[0],lat=lat,outfile='Tide_Maputo_18years.txt')
