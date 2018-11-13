import yaml
import numpy as np


def Sat_BRDF(dc, query, sat_array):
    
    #
    # Identify indexed data using find_datasets
    #
    data = dc.find_datasets(product='ls8_nbart_scene', 
                            time=(str(sat_array.time.values[0])),
                            lat=query['lat'], 
                            lon=query['lon'])
    # 
    # Use yaml to load in information on the Solar zenith angle at the time of
    # satellite overpass and BRDF data that was used to product the NBAR/T
    # product.
    #
    filelink = data[0]
    with open(filelink.uris[0][len('file://'):]) as fl:
        yamdoc = yaml.load(fl)
        
    #
    # Solar zenith at time of satellite overpass is extracted here, but not
    # used. So this is just a placeholder, should it be needed in the future.
    #
    solar_zenith = 90-yamdoc['lineage']['source_datasets']['level1']['image']['sun_elevation']
    
    params = yamdoc['lineage']['algorithm']['parameters']
    
    #
    # NOTE: band order looks messed up. But this is because it gets re-messed
    # when later on deciding whether to apply BRDF to Landsat or Sentinel bands
    #
    brdf_sat_data = np.array([['', 'brdf0', 'brdf1', 'brdf2'],
                              ['band1', params['band_1_brdf_iso'], params['band_1_brdf_vol'],params['band_1_brdf_geo']],
                              ['band2', params['band_2_brdf_iso'], params['band_2_brdf_vol'],params['band_2_brdf_geo']],
                              ['band3', params['band_3_brdf_iso'], params['band_3_brdf_vol'],params['band_3_brdf_geo']],
                              ['band4', params['band_4_brdf_iso'], params['band_4_brdf_vol'],params['band_4_brdf_geo']],
                              ['band5', params['band_5_brdf_iso'], params['band_5_brdf_vol'],params['band_5_brdf_geo']],
                              ['band6', params['band_6_brdf_iso'], params['band_6_brdf_vol'],params['band_6_brdf_geo']],
                              ['band7', params['band_7_brdf_iso'], params['band_7_brdf_vol'],params['band_7_brdf_geo']],
                              ['band8', params['band_5_brdf_iso'], params['band_5_brdf_vol'],params['band_5_brdf_geo']],
                              ['band8a', params['band_7_brdf_iso'], params['band_7_brdf_vol'],params['band_7_brdf_geo']],
                              ['band11', params['band_6_brdf_iso'], params['band_6_brdf_vol'],params['band_6_brdf_geo']],
                              ['band12', params['band_7_brdf_iso'], params['band_7_brdf_vol'],params['band_7_brdf_geo']],
                             ])
    
    return brdf_sat_data
