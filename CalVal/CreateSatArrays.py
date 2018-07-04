import datacube


#
# Query Satellite data, based on manual input location and time
#
def create_sat_arrays(dc, query, query2, field_data):
    if field_data[3] == 'Sentinel2a':
        b_names = ['nbar_coastal_aerosol', 'nbar_blue', 'nbar_green', 'nbar_red', 'nbar_red_edge_1', 'nbar_red_edge_2', 'nbar_red_edge_3', 'nbar_nir_1', 'nbar_nir_2', 'nbar_swir_2', 'nbar_swir_3']
        sat_array = dc.load(product='s2a_510_granule', measurements=b_names, **query)
        sat_bigarray = dc.load(product='s2a_510_granule', measurements=b_names, **query2)
    
    elif field_data[3] == 'Sentinel2b':
        b_names = ['nbar_coastal_aerosol', 'nbar_blue', 'nbar_green', 'nbar_red', 'nbar_red_edge_1', 'nbar_red_edge_2', 'nbar_red_edge_3', 'nbar_nir_1', 'nbar_nir_2', 'nbar_swir_2', 'nbar_swir_3']
        sat_array = dc.load(product='s2b_510_granule', measurements=b_names, **query)
        sat_bigarray = dc.load(product='s2b_510_granule', measurements=b_names, **query2)
    
    elif field_data[3] == 'Landsat8':
        sat_array = dc.load(product='ls8_nbar_scene', **query)
        sat_bigarray = dc.load(product='ls8_nbar_scene', **query2)
        sat_array.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'}, inplace=True)
        sat_bigarray.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'}, inplace=True)

    else:
        print('Satellite must be one of Landsat8 or Sentinel2a/b. Got', field_data[3])

    return sat_array, sat_bigarray
