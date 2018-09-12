import numpy as np
import pandas as pd


#
# Create a statistics dataframe to compare field and satellite for a subset of pixels
#
def create_SUB_stats(sat_array, field_array, ground_brdf, fstat_df, field_data):

    subsat_array = sat_array.where(field_array*0 == 0)

    if field_data[3] == 'Landsat8':
        inner_array = np.array([['', 'Sat_inner_mean', 'Sat_SD', 'Field_inner_mean'],
                            ['Band1', float(subsat_array.coastal_aerosol[0].mean()/10000), float(subsat_array.coastal_aerosol[0].std()/10000), float(ground_brdf['band1'].mean())],
                            ['Band2', float(subsat_array.blue[0].mean()/10000), float(subsat_array.blue[0].std()/10000), float(ground_brdf['band2'].mean())],
                            ['Band3', float(subsat_array.green[0].mean()/10000), float(subsat_array.green[0].std()/10000), float(ground_brdf['band3'].mean())],
                            ['Band4', float(subsat_array.red[0].mean()/10000), float(subsat_array.red[0].std()/10000), float(ground_brdf['band4'].mean())],
                            ['Band5', float(subsat_array.nir[0].mean()/10000), float(subsat_array.nir[0].std()/10000), float(ground_brdf['band5'].mean())],
                            ['Band6', float(subsat_array.swir1[0].mean()/10000), float(subsat_array.swir1[0].std()/10000), float(ground_brdf['band6'].mean())],
                            ['Band7', float(subsat_array.swir2[0].mean()/10000), float(subsat_array.swir2[0].std()/10000), float(ground_brdf['band7'].mean())],
                           ])

    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        inner_array = np.array([['', 'Sat_inner_mean', 'Sat_SD', 'Field_inner_mean'],
                            ['Band1', float(subsat_array.nbart_coastal_aerosol[0].mean()/10000), float(subsat_array.nbart_coastal_aerosol[0].std()/10000), float(ground_brdf['band1'].mean())],
                            ['Band2', float(subsat_array.nbart_blue[0].mean()/10000), float(subsat_array.nbart_blue[0].std()/10000), float(ground_brdf['band2'].mean())],
                            ['Band3', float(subsat_array.nbart_green[0].mean()/10000), float(subsat_array.nbart_green[0].std()/10000), float(ground_brdf['band3'].mean())],
                            ['Band4', float(subsat_array.nbart_red[0].mean()/10000), float(subsat_array.nbart_red[0].std()/10000), float(ground_brdf['band4'].mean())],
                            ['Band5', float(subsat_array.nbart_red_edge_1[0].mean()/10000), float(subsat_array.nbart_red_edge_1[0].std()/10000), float(ground_brdf['band5'].mean())],
                            ['Band6', float(subsat_array.nbart_red_edge_2[0].mean()/10000), float(subsat_array.nbart_red_edge_2[0].std()/10000), float(ground_brdf['band6'].mean())],
                            ['Band7', float(subsat_array.nbart_red_edge_3[0].mean()/10000), float(subsat_array.nbart_red_edge_3[0].std()/10000), float(ground_brdf['band7'].mean())],
                            ['Band8', float(subsat_array.nbart_nir_1[0].mean()/10000), float(subsat_array.nbart_nir_1[0].std()/10000), float(ground_brdf['band8'].mean())],
                            ['Band8a', float(subsat_array.nbart_nir_2[0].mean()/10000), float(subsat_array.nbart_nir_2[0].std()/10000), float(ground_brdf['band8a'].mean())],
                            ['Band11', float(subsat_array.nbart_swir_2[0].mean()/10000), float(subsat_array.nbart_swir_2[0].std()/10000), float(ground_brdf['band11'].mean())],
                            ['Band12', float(subsat_array.nbart_swir_3[0].mean()/10000), float(subsat_array.nbart_swir_3[0].std()/10000), float(ground_brdf['band12'].mean())],
                           ])

    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    inner_df = pd.DataFrame(data=inner_array[1:,1:],
                      index=inner_array[1:,0],
                      columns=inner_array[0,1:])

    inner_df['Field_SD'] = fstat_df['Field_SD']

    finner_df = inner_df.astype(float)
    return finner_df
