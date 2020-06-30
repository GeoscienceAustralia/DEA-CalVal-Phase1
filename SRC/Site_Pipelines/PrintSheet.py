import pandas as pd

def print_sheet(ground_brdf, sat_array, fstat_df, indir, output, field_data, Corners, RockWalk, StartCorner, variance, query, dc):

    arr = variance.to_array()
    varr = arr.to_series()

    if field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        fstat_name = fstat_df.rename({'Band1': 'CA', 'Band2': 'blue', 'Band3': 'green', 'Band4': 'red', 
                                      'Band5': 'RE1', 'Band6': 'RE2', 'Band7': 'RE3', 
                                      'Band8': 'nir_1', 'Band8a': 'nir_2', 'Band11': 'swir_2', 'Band12': 'swir_3'})
        varr_name = varr.rename({'nbart_coastal_aerosol': 'CA', 'nbart_blue': 'blue', 'nbart_green': 'green',
                                 'nbart_red': 'red', 'nbart_red_edge_1': 'RE1', 'nbart_red_edge_2': 'RE2',
                                 'nbart_red_edge_3': 'RE3', 'nbart_nir_1': 'nir_1', 'nbart_nir_2': 'nir_2',
                                 'nbart_swir_2': 'swir_2', 'nbart_swir_3': 'swir_3'})
    elif field_data[3] == 'Landsat8':
        fstat_name = fstat_df.rename({'Band1': 'CA', 'Band2': 'blue', 'Band3': 'green', 'Band4': 'red',
                         'Band5': 'nir', 'Band6': 'swir1', 'Band7': 'swir2'})
        varr_name = varr.copy()
        varr_name = varr.rename({'coastal_aerosol': 'CA'})
    else:
        print('Satellite name should be one of Sentinel2a/b or Landsat8. I got ', field_data[3])

    snew = pd.concat([fstat_name, varr_name], axis=1)

    file = open(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'.txt', 'w')

    file.write('DATA SHEET FOR '+field_data[0]+' taken on '+field_data[1]+', '+field_data[2]+' '+field_data[3]+' overpass\n')
    file.write('------------------------------------------------------------------\n\n')
  
    if isinstance(ground_brdf['date_saved'].min(), pd.datetime):
        file.write(ground_brdf['date_saved'].min().strftime('Time of field site measurements is from %H:%M:%S'))
        file.write(ground_brdf['date_saved'].max().strftime(' to %H:%M:%S on the %d %B, %Y (UTC)')+'\n')
        file.write('Satellite overpass was at ' + str(sat_array.time.values[0]) + ' (UTC)\n\n')
        file.write('Difference in time between start of field site measurement\nand satellite overpass is ' + 
                   str(pd.to_datetime(str(sat_array.time.values[0])) - ground_brdf['date_saved'].min()) + '\n\n')
    else:
        file.write('Time of field site measurements is from'+ground_brdf['date_saved'].min())
        file.write('to '+ground_brdf['date_saved'].max()+'\n')
        file.write('Satellite overpass was at ' + str(sat_array.time.values[0]) + ' (UTC)\n\n')
        file.write('Difference in time between start of field site measurement\nand satellite overpass is ' + 
                   str(pd.to_datetime(str(sat_array.time.values[0])) - pd.to_datetime(ground_brdf['date_saved'].min())) + '\n\n')

    if Corners == [0, 0, 0, 0, 0, 0, 0, 0]:
        file.write('Good GPS Coordinates were found in the headers\n')
        file.write('Approximate bounding box coordinates:\n')
        file.write('NW: ('+str(round(ground_brdf['Longitude'].min(), 6))+', '+str(round(ground_brdf['Latitude'].max(), 6))+')\n\n')
        file.write('NE: ('+str(round(ground_brdf['Longitude'].max(), 6))+', '+str(round(ground_brdf['Latitude'].max(), 6))+')\n')
        file.write('SW: ('+str(round(ground_brdf['Longitude'].min(), 6))+', '+str(round(ground_brdf['Latitude'].min(), 6))+')\n')
        file.write('SE: ('+str(round(ground_brdf['Longitude'].max(), 6))+', '+str(round(ground_brdf['Latitude'].min(), 6))+')\n')
    else:
        file.write('NO GPS Coordinates found - coordinates have been approximated!!!\n')
        file.write('Approximate bounding box coordinates:\n')
        file.write('NW: ('+str(Corners[7])+', '+str(Corners[6])+')\n\n')
        file.write('NE: ('+str(Corners[5])+', '+str(Corners[4])+')\n')
        file.write('SW: ('+str(Corners[3])+', '+str(Corners[2])+')\n')
        file.write('SE: ('+str(Corners[1])+', '+str(Corners[0])+')\n')

    file.write('Solar Zenith angle is from ' + str(round(ground_brdf['Solar_angle'].max(), 1))
               + ' to ' + str(round(ground_brdf['Solar_angle'].min(), 1)) + ' degrees.\n\n')

    file.write('Data were read in from ' + indir + '\n')
    file.write('PNGs were written to ' + output + '\n\n')

    file.write('Panel is assumed to be ' + field_data[4] + '\n')
    file.write('Data is assumed to be recorded in ' + field_data[5] + ' mode.\n\n')

    exquery = dict()
    exquery['lat'] = query['lat']
    exquery['lon'] = query['lon']
    exquery['time'] = query['time']

    if field_data[3] == 'Sentinel2a':
        if field_data[6] == 'Sen2Cor':
            prod = 's2a_sen2cor_v6'
        else:
            prod = 's2a_ard_granule'
    elif field_data[3] == 'Sentinel2b':
        if field_data[6] == 'Sen2Cor':
            prod = 's2b_sen2cor_v1'
        else:
            prod = 's2b_ard_granule'
    elif field_data[3] == 'Landsat8':
        try:
            if field_data[7] == 'C6':
                prod = 'ga_ls8c_ard_3'
            else:
                prod = 'ls8_nbart_scene'
        except IndexError:
            prod = 'ls8_nbart_scene'
    else:
        print('The satellite should be one of Sentinel2a/b or Landsat8. I got ', field_data[3])

    file.write('Satellite processing and historical data can be found using the following dataset ID and location:\n'+str(dc.find_datasets(product=prod, **exquery))+'\n\n')

    file.write('Summary Statistics over entire field site:\n------------------------------------------\n\n')
    file.write('Band      Sat     Sat   Field    Field    Sat    Field  Sat/Fld Sat\n')
    file.write('         mean     rms    mean     rms  rms/mean rms/mean Ratio  Pixel-by-pixel\n')
    file.write('                                         (%)     (%)            rms (%)\n')

    file.close()

    snew.to_csv(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'.txt', header=None, sep='\t', float_format='%.3g', mode='a')

