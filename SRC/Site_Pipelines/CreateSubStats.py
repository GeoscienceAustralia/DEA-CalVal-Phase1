import numpy as np
import pandas as pd


#
# Create a statistics dataframe to compare field and satellite for a subset of pixels
#
def create_SUB_stats(ls_sat_array, s2_sat_array, ls_field_array, s2_field_array, ls_ground_brdf, s2_ground_brdf, ls_fstat_df, s2_fstat_df, field_data):

    ls_subsat_array = ls_sat_array.where(ls_field_array*0 == 0)
    s2_subsat_array = s2_sat_array.where(s2_field_array*0 == 0)

    ls_inner_array = np.array([['', 'Sat_inner_mean', 'Sat_SD', 'Field_inner_mean'],
                        ['Band1', float(ls_subsat_array.coastal_aerosol[0].mean()/10000), float(ls_subsat_array.coastal_aerosol[0].std()/10000), float(ls_ground_brdf['band1'].mean())],
                        ['Band2', float(ls_subsat_array.blue[0].mean()/10000), float(ls_subsat_array.blue[0].std()/10000), float(ls_ground_brdf['band2'].mean())],
                        ['Band3', float(ls_subsat_array.green[0].mean()/10000), float(ls_subsat_array.green[0].std()/10000), float(ls_ground_brdf['band3'].mean())],
                        ['Band4', float(ls_subsat_array.red[0].mean()/10000), float(ls_subsat_array.red[0].std()/10000), float(ls_ground_brdf['band4'].mean())],
                        ['Band5', float(ls_subsat_array.nir[0].mean()/10000), float(ls_subsat_array.nir[0].std()/10000), float(ls_ground_brdf['band5'].mean())],
                        ['Band6', float(ls_subsat_array.swir1[0].mean()/10000), float(ls_subsat_array.swir1[0].std()/10000), float(ls_ground_brdf['band6'].mean())],
                        ['Band7', float(ls_subsat_array.swir2[0].mean()/10000), float(ls_subsat_array.swir2[0].std()/10000), float(ls_ground_brdf['band7'].mean())],
                       ])

    if s2_sat_array.notnull():
        s2_inner_array = np.array([['', 'Sat_inner_mean', 'Sat_SD', 'Field_inner_mean'],
                            ['Band1', float(s2_subsat_array.nbart_coastal_aerosol[0].mean()/10000), float(s2_subsat_array.nbart_coastal_aerosol[0].std()/10000), float(s2_ground_brdf['band1'].mean())],
                            ['Band2', float(s2_subsat_array.nbart_blue[0].mean()/10000), float(s2_subsat_array.nbart_blue[0].std()/10000), float(s2_ground_brdf['band2'].mean())],
                            ['Band3', float(s2_subsat_array.nbart_green[0].mean()/10000), float(s2_subsat_array.nbart_green[0].std()/10000), float(s2_ground_brdf['band3'].mean())],
                            ['Band4', float(s2_subsat_array.nbart_red[0].mean()/10000), float(s2_subsat_array.nbart_red[0].std()/10000), float(s2_ground_brdf['band4'].mean())],
                            ['Band5', float(s2_subsat_array.nbart_red_edge_1[0].mean()/10000), float(s2_subsat_array.nbart_red_edge_1[0].std()/10000), float(s2_ground_brdf['band5'].mean())],
                            ['Band6', float(s2_subsat_array.nbart_red_edge_2[0].mean()/10000), float(s2_subsat_array.nbart_red_edge_2[0].std()/10000), float(s2_ground_brdf['band6'].mean())],
                            ['Band7', float(s2_subsat_array.nbart_red_edge_3[0].mean()/10000), float(s2_subsat_array.nbart_red_edge_3[0].std()/10000), float(s2_ground_brdf['band7'].mean())],
                            ['Band8', float(s2_subsat_array.nbart_nir_1[0].mean()/10000), float(s2_subsat_array.nbart_nir_1[0].std()/10000), float(s2_ground_brdf['band8'].mean())],
                            ['Band8a', float(s2_subsat_array.nbart_nir_2[0].mean()/10000), float(s2_subsat_array.nbart_nir_2[0].std()/10000), float(s2_ground_brdf['band8a'].mean())],
                            ['Band11', float(s2_subsat_array.nbart_swir_2[0].mean()/10000), float(s2_subsat_array.nbart_swir_2[0].std()/10000), float(s2_ground_brdf['band11'].mean())],
                            ['Band12', float(s2_subsat_array.nbart_swir_3[0].mean()/10000), float(s2_subsat_array.nbart_swir_3[0].std()/10000), float(s2_ground_brdf['band12'].mean())],
                           ])

    ls_inner_df = pd.DataFrame(data=ls_inner_array[1:,1:],
                      index=ls_inner_array[1:,0],
                      columns=ls_inner_array[0,1:])

    if s2_sat_array.notnull():
        s2_inner_df = pd.DataFrame(data=s2_inner_array[1:,1:],
                          index=s2_inner_array[1:,0],
                          columns=s2_inner_array[0,1:])

    ls_inner_df['Field_SD'] = ls_fstat_df['Field_SD']
    if s2_sat_array.notnull():
        s2_inner_df['Field_SD'] = s2_fstat_df['Field_SD']

    ls_finner_df = ls_inner_df.astype(float)
    if s2_sat_array.notnull():
        s2_finner_df = s2_inner_df.astype(float)

    if s2_sat_array.notnull():
        return ls_finner_df, s2_finner_df
    else:
        return ls_finner_df, ls_finner_df
