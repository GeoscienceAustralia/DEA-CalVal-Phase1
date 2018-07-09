import numpy as np
import pandas as pd


#
# Create a statistics dataframe to compare field and satellite for a subset of pixels
#
def create_SUB_stats(sat_array, field_array, fstat_df, inpix, field_data):

    if field_data[3] == 'Landsat8':
        inner_array = np.array([['', 'Sat_inner_mean', 'Field_inner_mean'],
                            ['Band1', float(sat_array.coastal_aerosol[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.coastal_aerosol[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band2', float(sat_array.blue[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.blue[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band3', float(sat_array.green[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.green[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band4', float(sat_array.red[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.red[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band5', float(sat_array.nir[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nir[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band6', float(sat_array.swir1[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.swir1[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band7', float(sat_array.swir2[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.swir2[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                           ])

    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        inner_array = np.array([['', 'Sat_inner_mean', 'Field_inner_mean'],
                            ['Band1', float(sat_array.nbar_coastal_aerosol[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nbar_coastal_aerosol[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band2', float(sat_array.nbar_blue[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nbar_blue[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band3', float(sat_array.nbar_green[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nbar_green[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band4', float(sat_array.nbar_red[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nbar_red[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band5', float(sat_array.nbar_red_edge_1[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nbar_red_edge_1[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band6', float(sat_array.nbar_red_edge_2[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nbar_red_edge_2[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band7', float(sat_array.nbar_red_edge_3[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nbar_red_edge_3[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band8', float(sat_array.nbar_nir_1[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nbar_nir_1[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band8a', float(sat_array.nbar_nir_2[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nbar_nir_2[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band11', float(sat_array.nbar_swir_2[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nbar_swir_2[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band12', float(sat_array.nbar_swir_3[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nbar_swir_3[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                           ])

    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    inner_df = pd.DataFrame(data=inner_array[1:,1:],
                      index=inner_array[1:,0],
                      columns=inner_array[0,1:])

    inner_df['Field_SD'] = fstat_df['Field_SD']
    inner_df['Sat_SD'] = fstat_df['Sat_SD']

    finner_df = inner_df.astype(float)
    return finner_df
