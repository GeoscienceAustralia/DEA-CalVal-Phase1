import datacube
import pandas as pd


#
# Query Satellite data, based on manual input location and time
#
def create_sat_arrays(dc, udc, query, query2, field_data):

    sent_b_names = ['nbart_coastal_aerosol', 'nbart_blue', 'nbart_green',
                    'nbart_red', 'nbart_red_edge_1', 'nbart_red_edge_2',
                    'nbart_red_edge_3', 'nbart_nir_1', 'nbart_nir_2',
                    'nbart_swir_2', 'nbart_swir_3']

    sen2cor_b_names = ['B01_60m', 'B02_10m', 'B03_10m', 'B04_10m', 'B05_20m',
                       'B06_20m', 'B07_20m', 'B08_10m', 'B8A_20m', 'B11_20m',
                       'B12_20m']

    ls_b_names = ['nbart_coastal_aerosol', 'nbart_blue', 'nbart_green',
                  'nbart_red', 'nbart_nir', 'nbart_swir_1', 'nbart_swir_2']

    usgs_names = ['coastal_aerosol', 'blue', 'green', 'red', 'nir', 'swir1',
                  'swir2']

    if field_data[3] == 'Sentinel2a':

        if field_data[6] == 'Sen2Cor':
            sat_array = dc.load(product='s2a_sen2cor_v6', measurements=sen2cor_b_names, **query)
            sat_array = sen2cor_band_rename(sat_array)
            sat_bigarray = dc.load(product='s2a_sen2cor_v6', measurements=sen2cor_b_names, **query2)
            sat_bigarray = sen2cor_band_rename(sat_bigarray)

        else:
            sat_array = dc.load(product='s2a_ard_granule', measurements=sent_b_names, **query)
            sat_bigarray = dc.load(product='s2a_ard_granule', measurements=sent_b_names, **query2)
    
    elif field_data[3] == 'Sentinel2b':
        if field_data[6] == 'Sen2Cor':
            sat_array = dc.load(product='s2b_sen2cor_v1', measurements=sen2cor_b_names, **query)
            sat_array = sen2cor_band_rename(sat_array)
            sat_bigarray = dc.load(product='s2b_sen2cor_v1', measurements=sen2cor_b_names, **query2)
            sat_bigarray = sen2cor_band_rename(sat_bigarray)

        else:
            sat_array = dc.load(product='s2b_ard_granule', measurements=sent_b_names, **query)
            sat_bigarray = dc.load(product='s2b_ard_granule', measurements=sent_b_names, **query2)
    
    elif field_data[3] == 'Landsat8':
        try:
            if field_data[7] == 'C6':
                sat_array = dc.load(product='ga_ls8c_ard_3', measurements=ls_b_names, **query)
                sat_bigarray = dc.load(product='ga_ls8c_ard_3', measurements=ls_b_names, **query2)
                sat_array = lsC6_band_rename(sat_array)
                sat_bigarray = lsC6_band_rename(sat_bigarray)

            else:
                sat_array = dc.load(product='ls8_nbart_scene', **query)
                sat_bigarray = dc.load(product='ls8_nbart_scene', **query2)
                sat_array = ls_band_rename(sat_array)
                sat_bigarray = ls_band_rename(sat_bigarray)


        except IndexError:
            sat_array = dc.load(product='ls8_nbart_scene', **query)
            sat_bigarray = dc.load(product='ls8_nbart_scene', **query2)
            sat_array = ls_band_rename(sat_array)
            sat_bigarray = ls_band_rename(sat_bigarray)


        if field_data[6] == 'USGS':
            ls8_usgs_array = udc.load(product='ls8_usgs_l2c1', measurements=usgs_names, **query)
            ls8_usgs_bigarray = udc.load(product='ls8_usgs_l2c1', measurements=usgs_names, **query2)
            ls8_usgs_array = ls8_usgs_array.sel(time=[pd.Timestamp(field_data[1])], method='nearest')
            ls8_usgs_bigarray = ls8_usgs_bigarray.sel(time=[pd.Timestamp(field_data[1])], method='nearest')


    else:
        print('Satellite must be one of Landsat8 or Sentinel2a/b. Got', field_data[3])

    if sat_array.notnull():
        sat_array = sat_array.sel(time=[pd.Timestamp(field_data[1])], method='nearest')
        sat_bigarray = sat_bigarray.sel(time=[pd.Timestamp(field_data[1])], method='nearest')

    if field_data[3] == 'Landsat8':
        if field_data[6] == 'USGS':
            return sat_array, sat_bigarray, ls8_usgs_array, ls8_usgs_bigarray
        else:
            return sat_array, sat_bigarray, [0], [0]
    else:
        return sat_array, sat_bigarray


#
# For Sen2Cor processing, rename inbuilt band names to match normal processing
# names.
#
def sen2cor_band_rename(sat_array):
    return sat_array.rename({
                             'B01_60m': 'nbart_coastal_aerosol',
                             'B02_10m': 'nbart_blue',
                             'B03_10m': 'nbart_green',
                             'B04_10m': 'nbart_red',
                             'B05_20m': 'nbart_red_edge_1', 
                             'B06_20m': 'nbart_red_edge_2',
                             'B07_20m': 'nbart_red_edge_3',
                             'B08_10m': 'nbart_nir_1', 
                             'B8A_20m': 'nbart_nir_2', 
                             'B11_20m': 'nbart_swir_2',
                             'B12_20m': 'nbart_swir_3'
                            })


#
# For Landsat processing, rename inbuilt band names for Collection 6
#
def lsC6_band_rename(sat_array):
    return sat_array.rename({
                             'nbart_coastal_aerosol': 'coastal_aerosol',
                             'nbart_blue': 'blue',
                             'nbart_green': 'green',
                             'nbart_red': 'red',
                             'nbart_nir': 'nir',
                             'nbart_swir_1': 'swir1',
                             'nbart_swir_2': 'swir2'
                           })


#
# For Landsat processing, rename inbuilt band names for standard Collection 5
def ls_band_rename(sat_array):
    return sat_array.rename({
                             '1': 'coastal_aerosol',
                             '2': 'blue',
                             '3': 'green',
                             '4': 'red',
                             '5': 'nir',
                             '6': 'swir1',
                             '7': 'swir2'
                           })
