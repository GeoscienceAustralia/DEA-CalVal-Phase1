import yaml
import numpy as np
import pandas as pd


def Sat_BRDF(dc, query, sat_array, field_data):
    
    #
    # Identify indexed data using find_datasets
    #
    data = dc.find_datasets(product='ga_ls8c_ard_3', 
                            time=(str(sat_array.time.values[0])),
                            lat=query['lat'], 
                            lon=query['lon'])
    # 
    # Use yaml to load in information on the Solar zenith angle at the time of
    # satellite overpass and BRDF data that was used to product the NBAR/T
    # product.
    #
    filelink = data[0]

    try:
        with open(filelink.uris[0][len('file://'):]) as fl:
            yamdoc = yaml.load(fl, Loader=yaml.FullLoader)
        with open(filelink.uris[0][len('file://'):].replace('odc-metadata', 'proc-info')) as fl2:
            yamdoc2 = yaml.load(fl2, Loader=yaml.FullLoader)
        
    except IndexError:
        with open(filelink.uris[0][len('file://'):]) as fl:
            yamdoc = yaml.load(fl, Loader=yaml.FullLoader)
        print('Got the index error')
        
    #
    # Solar zenith at time of satellite overpass is extracted here.
    #
    solar_zenith = 90 - yamdoc['properties']['eo:sun_elevation']
    brdfs = yamdoc2['wagl']['ancillary']['brdf']
    brdf_sat_data = np.array([['', 'brdf0', 'brdf1', 'brdf2'],
                      ['band1', 1, brdfs['alpha_1']['band_1'],brdfs['alpha_2']['band_1']],
                      ['band2', 1, brdfs['alpha_1']['band_2'],brdfs['alpha_2']['band_2']],
                      ['band3', 1, brdfs['alpha_1']['band_3'],brdfs['alpha_2']['band_3']],
                      ['band4', 1, brdfs['alpha_1']['band_4'],brdfs['alpha_2']['band_4']],
                      ['band5', 1, brdfs['alpha_1']['band_5'],brdfs['alpha_2']['band_5']],
                      ['band6', 1, brdfs['alpha_1']['band_6'],brdfs['alpha_2']['band_6']],
                      ['band7', 1, brdfs['alpha_1']['band_7'],brdfs['alpha_2']['band_7']],
                      ['band8', 1, brdfs['alpha_1']['band_5'],brdfs['alpha_2']['band_5']],
                      ['band8a', 1, brdfs['alpha_1']['band_7'],brdfs['alpha_2']['band_7']],
                      ['band11', 1, brdfs['alpha_1']['band_6'],brdfs['alpha_2']['band_6']],
                      ['band12', 1, brdfs['alpha_1']['band_7'],brdfs['alpha_2']['band_7']],
                     ])

    #
    # NOTE: band order looks messed up. But this is because it gets re-messed
    # when later on deciding whether to apply BRDF to Landsat or Sentinel bands
    #
    
    return pd.DataFrame(data=brdf_sat_data[1:,1:], index=brdf_sat_data[1:,0], columns=brdf_sat_data[0,1:]), solar_zenith

    #return brdf_sat_data, solar_zenith
