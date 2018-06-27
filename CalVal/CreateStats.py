import numpy as np
import pandas as pd


#
### Create statistics dataframe, comparing satellite and field data
#
def create_stats(sat_array, ground_brdf):
    data_array = np.array([['','LS8_mean','LS8_SD', 'Field_mean', 'Field_SD'],
                    ['Band1', float(sat_array.coastal_aerosol.mean()/10000), float(sat_array.coastal_aerosol.std()/10000), float(ground_brdf['band1'].mean()), float(ground_brdf['band1'].std())],
                    ['Band2', float(sat_array.blue.mean()/10000), float(sat_array.blue.std()/10000), float(ground_brdf['band2'].mean()), float(ground_brdf['band2'].std())],
                    ['Band3', float(sat_array.green.mean()/10000), float(sat_array.green.std()/10000), float(ground_brdf['band3'].mean()), float(ground_brdf['band3'].std())],
                    ['Band4', float(sat_array.red.mean()/10000), float(sat_array.red.std()/10000), float(ground_brdf['band4'].mean()), float(ground_brdf['band4'].std())],
                    ['Band5', float(sat_array.nir.mean()/10000), float(sat_array.nir.std()/10000), float(ground_brdf['band5'].mean()), float(ground_brdf['band5'].std())],
                    ['Band6', float(sat_array.swir1.mean()/10000), float(sat_array.swir1.std()/10000), float(ground_brdf['band6'].mean()), float(ground_brdf['band6'].std())],
                    ['Band7', float(sat_array.swir2.mean()/10000), float(sat_array.swir2.std()/10000), float(ground_brdf['band7'].mean()), float(ground_brdf['band7'].std())],
                    ])

    stat_df = pd.DataFrame(data=data_array[1:,1:],
                      index=data_array[1:,0],
                      columns=data_array[0,1:])

    stat_df['LS8_SD/mean (%)'] = 100*stat_df['LS8_SD'].astype(float)/stat_df['LS8_mean'].astype(float)
    stat_df['Field_SD/mean (%)'] = 100*stat_df['Field_SD'].astype(float)/stat_df['Field_mean'].astype(float)
    stat_df['LS8/Field'] = stat_df['LS8_mean'].astype(float)/stat_df['Field_mean'].astype(float) 

    fstat_df = stat_df.astype(float)
    return fstat_df
