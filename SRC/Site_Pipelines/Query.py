import datacube
import math
import pandas as pd

def make_query(ground_brdf, field_data):
    
    udc = datacube.Datacube(env='ardinteroperability', config='/home/547/aw3463/.sent2.conf')
    try:
        if field_data[7] == 'C6':
            dc = datacube.Datacube(env='c3-samples')
        elif field_data[6] == 'Sen2Cor':
            dc = datacube.Datacube(config='/g/data/up71/projects/ESA_L2A_index/test-DataCube/lanwei_ard.conf')
        else:
            dc = datacube.Datacube()
    except IndexError:
        dc = datacube.Datacube()

    #
    # Test for Landsat 8 data
    #
    if field_data[3] == 'Landsat8':
        #
        # Set pixel size to 30m if Collection 6 data, otherwise set to 25m.
        #
        try:
            if field_data[7] == 'C6':
                pixsize = 30.0
            else:
                pixsize = 25.0
        except IndexError:
            pixsize = 25.0
    #
    # Test for Sentinel data and set pixsize to 10m
    #
    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        pixsize = 10.0
    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    # convert half a pixel in metres to decimal degrees latitude
    met_latdeg = (pixsize) / (2*111319.9)

    # convert half a pixel in metres to decimal degrees longitude
    met_londeg = met_latdeg / math.cos(math.radians(ground_brdf['Latitude'].mean()))

    # Test for unusual timestamp from Litchfield site
    if 'Z' in str(ground_brdf['date_saved'].min()):
        mintime = pd.Timestamp(ground_brdf['date_saved'].min())
        maxtime = pd.Timestamp(ground_brdf['date_saved'].max())
    else:
        mintime = ground_brdf['date_saved'].min()
        maxtime = ground_brdf['date_saved'].max()

    query = {
             'time': (mintime-pd.DateOffset(15), maxtime+pd.DateOffset(15)),
             'lat': (ground_brdf['Latitude'].min() - met_latdeg, ground_brdf['Latitude'].max() + met_latdeg),
             'lon': (ground_brdf['Longitude'].min() - met_londeg, ground_brdf['Longitude'].max() + met_londeg),
             'output_crs': 'EPSG:3577',
             'resampling': 'bilinear',
            }
    
    query2 = {
              'time': (mintime-pd.DateOffset(15), maxtime+pd.DateOffset(15)),
             'lat': (ground_brdf['Latitude'].min() - 0.01, ground_brdf['Latitude'].max() + 0.01),
             'lon': (ground_brdf['Longitude'].min() - 0.01, ground_brdf['Longitude'].max() + 0.01),
              'output_crs': 'EPSG:3577',
             'resampling': 'bilinear',
             }

    query['resolution'] = (-pixsize, pixsize)
    query2['resolution'] = (-pixsize, pixsize)
        
    return dc, udc, query, query2
