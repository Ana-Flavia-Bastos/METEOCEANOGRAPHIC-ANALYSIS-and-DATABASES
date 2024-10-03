import cdsapi

def ERA5_API_request(path,year,north,south,west,east):

    c=cdsapi.Client(url= 'https://cds.climate.copernicus.eu/api/v2',key='284568:f502128a-90af-406c-a7b8-de4a7dc64c09')
    print('Retriving years: '+ str(year))
    c.retrieve('reanalysis-era5-single-levels',
            {
                'product_type':'reanalysis',
                'format':'netcdf',
                'variable':[
                        'significant_height_of_combined_wind_waves_and_swell','peak_wave_period','mean_wave_direction'
                ],
                'year': '{}'.format(year),
                'month':[
                    '01','02','03',
                    '04','05','06',
                    '07','08','09',
                    '10','11','12',
                ],
                'day':[
                    '01','02','03',
                    '04','05','06',
                    '07','08','09',
                    '10','11','12',
                    '13','14','15',
                    '16','17','18',
                    '19','20','21',
                    '22','23','24',
                    '25','26','27',
                    '28','29','30',
                    '31',
                ],
                'time':[
                    '00:00','01:00','02:00',
                    '03:00','04:00','05:00',
                    '06:00','07:00','08:00',
                    '09:00','10:00','11:00',
                    '12:00','13:00','14:00',
                    '15:00','16:00','17:00',
                    '18:00','19:00','20:00',
                    '21:00','22:00','23:00',
                ],
                'area':[
                    north,west,south,east
                ],
            },
            path+'{}-{}_wavetotal.nc'.format(year,year+1))
