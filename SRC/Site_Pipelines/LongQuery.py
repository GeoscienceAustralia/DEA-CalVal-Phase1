import datacube
import math
import pandas as pd

def make_long_query(ground_brdf):
    
    ldc = datacube.Datacube()
    lpixsize = 25.0
    sdc = datacube.Datacube()
    spixsize = 10.0

    # convert half a pixel in metres to decimal degrees latitude
    lmet_latdeg = (lpixsize) / (2*111319.9)
    smet_latdeg = (spixsize) / (2*111319.9)

    # convert half a pixel in metres to decimal degrees longitude
    lmet_londeg = lmet_latdeg / math.cos(math.radians(ground_brdf['Latitude'].mean()))
    smet_londeg = smet_latdeg / math.cos(math.radians(ground_brdf['Latitude'].mean()))

    lquery = {
             'time': ('2013-01-01', '2118-12-31'),
             'lat': (ground_brdf['Latitude'].min() - lmet_latdeg, ground_brdf['Latitude'].max() + lmet_latdeg),
             'lon': (ground_brdf['Longitude'].min() - lmet_londeg, ground_brdf['Longitude'].max() + lmet_londeg),
             'output_crs': 'EPSG:3577',
             'resampling': 'bilinear',
             'group_by': 'solar_day',
            }
    
    squery = {
             'time': ('2013-01-01', '2118-12-31'),
             'lat': (ground_brdf['Latitude'].min() - smet_latdeg, ground_brdf['Latitude'].max() + smet_latdeg),
             'lon': (ground_brdf['Longitude'].min() - smet_londeg, ground_brdf['Longitude'].max() + smet_londeg),
             'output_crs': 'EPSG:3577',
             'resampling': 'bilinear',
             'group_by': 'solar_day',
            }
    
    lquery2 = {
             'time': ('2013-01-01', '2118-12-31'),
             'lat': (ground_brdf['Latitude'].min() - lmet_latdeg - 0.01, ground_brdf['Latitude'].max() + lmet_latdeg + 0.01),
             'lon': (ground_brdf['Longitude'].min() - lmet_londeg - 0.01, ground_brdf['Longitude'].max() + lmet_londeg + 0.01),
             'output_crs': 'EPSG:3577',
             'resampling': 'bilinear',
             'group_by': 'solar_day',
            }
    
    squery2 = {
             'time': ('2013-01-01', '2118-12-31'),
             'lat': (ground_brdf['Latitude'].min() - smet_latdeg - 0.01, ground_brdf['Latitude'].max() + smet_latdeg + 0.01),
             'lon': (ground_brdf['Longitude'].min() - smet_londeg - 0.01, ground_brdf['Longitude'].max() + smet_londeg + 0.01),
             'output_crs': 'EPSG:3577',
             'resampling': 'bilinear',
             'group_by': 'solar_day',
            }
    
    lquery['resolution'] = (-lpixsize, lpixsize)
    squery['resolution'] = (-spixsize, spixsize)
    lquery2['resolution'] = (-lpixsize, lpixsize)
    squery2['resolution'] = (-spixsize, spixsize)
        
    return ldc, sdc, lquery, squery, lquery2, squery2
