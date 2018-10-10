import numpy as np
import pandas as pd


#
### Create statistics dataframe, comparing satellite and field data
#
def create_stats(sat_array, ground_brdf, field_data):
    if field_data[3] == 'Landsat8':
        data_array = np.array([['','Sat_mean','Sat_SD', 'Field_mean', 'Field_SD'],
                        ['Band1', float(sat_array.coastal_aerosol.mean()/10000), float(sat_array.coastal_aerosol.std()/10000), float(ground_brdf['band1'].mean()), float(ground_brdf['band1'].std())],
                        ['Band2', float(sat_array.blue.mean()/10000), float(sat_array.blue.std()/10000), float(ground_brdf['band2'].mean()), float(ground_brdf['band2'].std())],
                        ['Band3', float(sat_array.green.mean()/10000), float(sat_array.green.std()/10000), float(ground_brdf['band3'].mean()), float(ground_brdf['band3'].std())],
                        ['Band4', float(sat_array.red.mean()/10000), float(sat_array.red.std()/10000), float(ground_brdf['band4'].mean()), float(ground_brdf['band4'].std())],
                        ['Band5', float(sat_array.nir.mean()/10000), float(sat_array.nir.std()/10000), float(ground_brdf['band5'].mean()), float(ground_brdf['band5'].std())],
                        ['Band6', float(sat_array.swir1.mean()/10000), float(sat_array.swir1.std()/10000), float(ground_brdf['band6'].mean()), float(ground_brdf['band6'].std())],
                        ['Band7', float(sat_array.swir2.mean()/10000), float(sat_array.swir2.std()/10000), float(ground_brdf['band7'].mean()), float(ground_brdf['band7'].std())],
                        ])

    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        data_array = np.array([['','Sat_mean','Sat_SD', 'Field_mean', 'Field_SD'],
                        ['Band1', float(sat_array.nbart_coastal_aerosol.mean()/10000), float(sat_array.nbart_coastal_aerosol.std()/10000), float(ground_brdf['band1'].mean()), float(ground_brdf['band1'].std())],
                        ['Band2', float(sat_array.nbart_blue.mean()/10000), float(sat_array.nbart_blue.std()/10000), float(ground_brdf['band2'].mean()), float(ground_brdf['band2'].std())],
                        ['Band3', float(sat_array.nbart_green.mean()/10000), float(sat_array.nbart_green.std()/10000), float(ground_brdf['band3'].mean()), float(ground_brdf['band3'].std())],
                        ['Band4', float(sat_array.nbart_red.mean()/10000), float(sat_array.nbart_red.std()/10000), float(ground_brdf['band4'].mean()), float(ground_brdf['band4'].std())],
                        ['Band5', float(sat_array.nbart_red_edge_1.mean()/10000), float(sat_array.nbart_red_edge_1.std()/10000), float(ground_brdf['band5'].mean()), float(ground_brdf['band5'].std())],
                        ['Band6', float(sat_array.nbart_red_edge_2.mean()/10000), float(sat_array.nbart_red_edge_2.std()/10000), float(ground_brdf['band6'].mean()), float(ground_brdf['band6'].std())],
                        ['Band7', float(sat_array.nbart_red_edge_3.mean()/10000), float(sat_array.nbart_red_edge_3.std()/10000), float(ground_brdf['band7'].mean()), float(ground_brdf['band7'].std())],
                        ['Band8', float(sat_array.nbart_nir_1.mean()/10000), float(sat_array.nbart_nir_1.std()/10000), float(ground_brdf['band8'].mean()), float(ground_brdf['band8'].std())],
                        ['Band8a', float(sat_array.nbart_nir_2.mean()/10000), float(sat_array.nbart_nir_2.std()/10000), float(ground_brdf['band8a'].mean()), float(ground_brdf['band8a'].std())],
                        ['Band11', float(sat_array.nbart_swir_2.mean()/10000), float(sat_array.nbart_swir_2.std()/10000), float(ground_brdf['band11'].mean()), float(ground_brdf['band11'].std())],
                        ['Band12', float(sat_array.nbart_swir_3.mean()/10000), float(sat_array.nbart_swir_3.std()/10000), float(ground_brdf['band12'].mean()), float(ground_brdf['band12'].std())],
                        ])

    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    stat_df = pd.DataFrame(data=data_array[1:,1:],
                      index=data_array[1:,0],
                      columns=data_array[0,1:])

    stat_df['Sat_SD/mean (%)'] = 100*stat_df['Sat_SD'].astype(float)/stat_df['Sat_mean'].astype(float)
    stat_df['Field_SD/mean (%)'] = 100*stat_df['Field_SD'].astype(float)/stat_df['Field_mean'].astype(float)
    stat_df['Sat/Field'] = stat_df['Sat_mean'].astype(float)/stat_df['Field_mean'].astype(float) 

    fstat_df = stat_df.astype(float)
    return fstat_df
