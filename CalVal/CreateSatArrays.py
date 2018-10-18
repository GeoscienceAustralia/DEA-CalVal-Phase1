import datacube
import pandas as pd


#
# Query Satellite data, based on manual input location and time
#
def create_sat_arrays(dc, query, query2, field_data):
    if field_data[3] == 'Sentinel2a':
        b_names = ['nbart_coastal_aerosol', 'nbart_blue', 'nbart_green', 'nbart_red', 'nbart_red_edge_1', 'nbart_red_edge_2', 'nbart_red_edge_3', 'nbart_nir_1', 'nbart_nir_2', 'nbart_swir_2', 'nbart_swir_3']
        sat_array = dc.load(product='s2a_ard_granule', measurements=b_names, **query)
        sat_bigarray = dc.load(product='s2a_ard_granule', measurements=b_names, **query2)
    
    elif field_data[3] == 'Sentinel2b':
        b_names = ['nbart_coastal_aerosol', 'nbart_blue', 'nbart_green', 'nbart_red', 'nbart_red_edge_1', 'nbart_red_edge_2', 'nbart_red_edge_3', 'nbart_nir_1', 'nbart_nir_2', 'nbart_swir_2', 'nbart_swir_3']
        sat_array = dc.load(product='s2b_ard_granule', measurements=b_names, **query)
        sat_bigarray = dc.load(product='s2b_ard_granule', measurements=b_names, **query2)
    
    elif field_data[3] == 'Landsat8':
        sat_array = dc.load(product='ls8_nbart_scene', **query)
        sat_bigarray = dc.load(product='ls8_nbart_scene', **query2)
        sat_array.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'}, inplace=True)
        sat_bigarray.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'}, inplace=True)

    else:
        print('Satellite must be one of Landsat8 or Sentinel2a/b. Got', field_data[3])

    #sat_array = sat_array.isel(time=[0])
    #sat_bigarray = sat_bigarray.isel(time=[0])
    sat_array = sat_array.sel(time=[pd.Timestamp(field_data[1])], method='nearest')
    sat_bigarray = sat_bigarray.sel(time=[pd.Timestamp(field_data[1])], method='nearest')

    return sat_array, sat_bigarray
