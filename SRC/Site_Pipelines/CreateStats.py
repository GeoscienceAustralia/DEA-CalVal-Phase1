import numpy as np
import pandas as pd


#
### Create statistics dataframe, comparing satellite and field data
#
def create_stats(ls_sat_array, s2_sat_array, ls_ground_brdf, s2_ground_brdf, field_data):

    ls_data_array = np.array([['','Sat_mean','Sat_SD', 'Field_mean', 'Field_SD'],
                    ['Band1', float(ls_sat_array.coastal_aerosol.mean()/10000), float(ls_sat_array.coastal_aerosol.std()/10000), float(ls_ground_brdf['band1'].mean()), float(ls_ground_brdf['band1'].std())],
                    ['Band2', float(ls_sat_array.blue.mean()/10000), float(ls_sat_array.blue.std()/10000), float(ls_ground_brdf['band2'].mean()), float(ls_ground_brdf['band2'].std())],
                    ['Band3', float(ls_sat_array.green.mean()/10000), float(ls_sat_array.green.std()/10000), float(ls_ground_brdf['band3'].mean()), float(ls_ground_brdf['band3'].std())],
                    ['Band4', float(ls_sat_array.red.mean()/10000), float(ls_sat_array.red.std()/10000), float(ls_ground_brdf['band4'].mean()), float(ls_ground_brdf['band4'].std())],
                    ['Band5', float(ls_sat_array.nir.mean()/10000), float(ls_sat_array.nir.std()/10000), float(ls_ground_brdf['band5'].mean()), float(ls_ground_brdf['band5'].std())],
                    ['Band6', float(ls_sat_array.swir1.mean()/10000), float(ls_sat_array.swir1.std()/10000), float(ls_ground_brdf['band6'].mean()), float(ls_ground_brdf['band6'].std())],
                    ['Band7', float(ls_sat_array.swir2.mean()/10000), float(ls_sat_array.swir2.std()/10000), float(ls_ground_brdf['band7'].mean()), float(ls_ground_brdf['band7'].std())],
                    ])

    if s2_sat_array.notnull():
        s2_data_array = np.array([['','Sat_mean','Sat_SD', 'Field_mean', 'Field_SD'],
                        ['Band1', float(s2_sat_array.nbart_coastal_aerosol.mean()/10000), float(s2_sat_array.nbart_coastal_aerosol.std()/10000), float(s2_ground_brdf['band1'].mean()), float(s2_ground_brdf['band1'].std())],
                        ['Band2', float(s2_sat_array.nbart_blue.mean()/10000), float(s2_sat_array.nbart_blue.std()/10000), float(s2_ground_brdf['band2'].mean()), float(s2_ground_brdf['band2'].std())],
                        ['Band3', float(s2_sat_array.nbart_green.mean()/10000), float(s2_sat_array.nbart_green.std()/10000), float(s2_ground_brdf['band3'].mean()), float(s2_ground_brdf['band3'].std())],
                        ['Band4', float(s2_sat_array.nbart_red.mean()/10000), float(s2_sat_array.nbart_red.std()/10000), float(s2_ground_brdf['band4'].mean()), float(s2_ground_brdf['band4'].std())],
                        ['Band5', float(s2_sat_array.nbart_red_edge_1.mean()/10000), float(s2_sat_array.nbart_red_edge_1.std()/10000), float(s2_ground_brdf['band5'].mean()), float(s2_ground_brdf['band5'].std())],
                        ['Band6', float(s2_sat_array.nbart_red_edge_2.mean()/10000), float(s2_sat_array.nbart_red_edge_2.std()/10000), float(s2_ground_brdf['band6'].mean()), float(s2_ground_brdf['band6'].std())],
                        ['Band7', float(s2_sat_array.nbart_red_edge_3.mean()/10000), float(s2_sat_array.nbart_red_edge_3.std()/10000), float(s2_ground_brdf['band7'].mean()), float(s2_ground_brdf['band7'].std())],
                        ['Band8', float(s2_sat_array.nbart_nir_1.mean()/10000), float(s2_sat_array.nbart_nir_1.std()/10000), float(s2_ground_brdf['band8'].mean()), float(s2_ground_brdf['band8'].std())],
                        ['Band8a', float(s2_sat_array.nbart_nir_2.mean()/10000), float(s2_sat_array.nbart_nir_2.std()/10000), float(s2_ground_brdf['band8a'].mean()), float(s2_ground_brdf['band8a'].std())],
                        ['Band11', float(s2_sat_array.nbart_swir_2.mean()/10000), float(s2_sat_array.nbart_swir_2.std()/10000), float(s2_ground_brdf['band11'].mean()), float(s2_ground_brdf['band11'].std())],
                        ['Band12', float(s2_sat_array.nbart_swir_3.mean()/10000), float(s2_sat_array.nbart_swir_3.std()/10000), float(s2_ground_brdf['band12'].mean()), float(s2_ground_brdf['band12'].std())],
                        ])

    ls_stat_df = pd.DataFrame(data=ls_data_array[1:,1:],
                      index=ls_data_array[1:,0],
                      columns=ls_data_array[0,1:])

    if s2_sat_array.notnull():
        s2_stat_df = pd.DataFrame(data=s2_data_array[1:,1:],
                          index=s2_data_array[1:,0],
                          columns=s2_data_array[0,1:])

    ls_stat_df['Sat_SD/mean (%)'] = 100*ls_stat_df['Sat_SD'].astype(float)/ls_stat_df['Sat_mean'].astype(float)
    ls_stat_df['Field_SD/mean (%)'] = 100*ls_stat_df['Field_SD'].astype(float)/ls_stat_df['Field_mean'].astype(float)
    ls_stat_df['Sat/Field'] = ls_stat_df['Sat_mean'].astype(float)/ls_stat_df['Field_mean'].astype(float) 

    if s2_sat_array.notnull():
        s2_stat_df['Sat_SD/mean (%)'] = 100*s2_stat_df['Sat_SD'].astype(float)/s2_stat_df['Sat_mean'].astype(float)
        s2_stat_df['Field_SD/mean (%)'] = 100*s2_stat_df['Field_SD'].astype(float)/s2_stat_df['Field_mean'].astype(float)
        s2_stat_df['Sat/Field'] = s2_stat_df['Sat_mean'].astype(float)/s2_stat_df['Field_mean'].astype(float) 

    ls_fstat_df = ls_stat_df.astype(float)
    if s2_sat_array.notnull():
        s2_fstat_df = s2_stat_df.astype(float)

    if s2_sat_array.notnull():
        return ls_fstat_df, s2_fstat_df
    else:
        return ls_fstat_df, ls_fstat_df
