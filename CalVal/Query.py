import datacube

def make_query(timerange, latrange, lonrange, field_data):
    query = {
             'time': timerange,
             'lat': latrange,
             'lon': lonrange,
             'output_crs': 'EPSG:3577',
            }
    
    query2 = {
              'time': timerange,
              'lat': (latrange[0]-0.01, latrange[1]+0.01),
              'lon': (lonrange[0]-0.01, lonrange[1]+0.01),
              'output_crs': 'EPSG:3577',
             }

    if field_data[3] == 'Landsat8':
        dc = datacube.Datacube()
        query['resolution'] = (-25, 25)
        query2['resolution'] = (-25, 25)
    
    elif field_data[3] == 'Sentinel2a' or 'Sentinel2b':
        dc = datacube.Datacube(config='/home/547/aw3463/.sent2.conf', env='sentinel2beta')
        query['resolution'] = (-10, 10)
        query2['resolution'] = (-10, 10)
    
    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])
        
    return dc, query, query2
