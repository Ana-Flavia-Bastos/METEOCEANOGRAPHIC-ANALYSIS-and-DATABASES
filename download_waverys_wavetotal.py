import copernicusmarine as cm
import math

def WAVERYS_API_request(path,initial_year,final_year,north,south,west,east):

  print('Retriving: '+ str(initial_year)+'-'+str(final_year))
  
  cm.subset(
    dataset_id="cmems_mod_glo_wav_my_0.2deg_PT3H-i",
    dataset_version="202311",
    variables=["VHM0", "VMDR", "VTPK"],
    minimum_longitude=west,
    maximum_longitude=east,
    minimum_latitude=south,
    maximum_latitude=north,
    start_datetime=str(initial_year)+"-01-01T00:00:00",
    end_datetime=str(final_year)+"-12-31T21:00:00",
    force_download=True,
    output_directory = path,
    #Download complete grid:
    #output_filename = '{}-{}_wavetotal.nc'.format(initial_year,final_year),
    #Download multiples points:
    output_filename = '{}-{}_wavetotal_{}_{}.nc'.format(initial_year,final_year,math.ceil(south),math.ceil(west)),
    #disable_progress_bar=False,
    credentials_file='C:\\Users\\test\\.copernicusmarine\\.copernicusmarine-credentials')