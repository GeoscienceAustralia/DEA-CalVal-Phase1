import datacube
import math

def make_query(timerange, ground_brdf, field_data):
    
    if field_data[3] == 'Landsat8':
        dc = datacube.Datacube()
        pixsize = 25.0
    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        dc = datacube.Datacube(config='/home/547/aw3463/.sent2.conf', env='sentinel2beta')
        pixsize = 10.0
    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    # convert half a pixel in metres to decimal degrees latitude
    met_latdeg = (pixsize) / (2*111319.9)

    # convert half a pixel in metres to decimal degrees longitude
    met_londeg = met_latdeg / math.cos(math.radians(ground_brdf['Latitude'].mean()))

    query = {
             'time': timerange,
             'lat': (ground_brdf['Latitude'].min() - met_latdeg, ground_brdf['Latitude'].max() + met_latdeg),
             'lon': (ground_brdf['Longitude'].min() - met_londeg, ground_brdf['Longitude'].max() + met_londeg),
             'output_crs': 'EPSG:3577',
            }
    
    query2 = {
              'time': timerange,
             'lat': (ground_brdf['Latitude'].min() - 0.01, ground_brdf['Latitude'].max() + 0.01),
             'lon': (ground_brdf['Longitude'].min() - 0.01, ground_brdf['Longitude'].max() + 0.01),
              'output_crs': 'EPSG:3577',
             }

    query['resolution'] = (-pixsize, pixsize)
    query2['resolution'] = (-pixsize, pixsize)
        
    return dc, query, query2
