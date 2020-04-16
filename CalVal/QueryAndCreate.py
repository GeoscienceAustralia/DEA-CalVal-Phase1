from . import Query
from . import CreateSatArrays
from . import SatBRDF
from . import BRDF
from . import FudgeGPS


def query_and_create(ls_ground_brdf, s2_ground_brdf, ls_ground_bands, s2_ground_bands, field_data, Corners, RockWalk, StartCorner):

    if len(field_data) < 8:
        print('Warning: field_data is less than 8 fields. This may mess up sen2cor processing')

    if field_data[3] == 'Landsat8':
        ls_dc, ls_udc, ls_query, ls_query2 = Query.make_query(ls_ground_brdf, field_data)
        s2_dc, s2_udc, s2_query, s2_query2 = Query.make_query(s2_ground_brdf, ['','','','Sentinel2a','','','',''])
    else:
        ls_dc, ls_udc, ls_query, ls_query2 = Query.make_query(ls_ground_brdf, ['','','','Landsat8','','','',''])
        s2_dc, s2_udc, s2_query, s2_query2 = Query.make_query(s2_ground_brdf, field_data)
    
        
    if field_data[3] == 'Landsat8':
        ls_sat_array, ls_sat_bigarray, ls8_usgs_array, ls8_usgs_bigarray = \
        CreateSatArrays.create_sat_arrays(ls_dc, ls_udc, ls_query, ls_query2, field_data)
        
        s2_sat_array, s2_sat_bigarray = \
        CreateSatArrays.create_sat_arrays(s2_dc, s2_udc, s2_query, s2_query2, ['','','','Sentinel2a','','','',''])

    else:
        s2_sat_array, s2_sat_bigarray = \
        CreateSatArrays.create_sat_arrays(s2_dc, s2_udc, s2_query, s2_query2, field_data)

        ls_sat_array, ls_sat_bigarray, ls8_usgs_array, ls8_usgs_bigarray = \
        CreateSatArrays.create_sat_arrays(ls_dc, ls_udc, ls_query, ls_query2, ['','','','Landsat8','','','',''])

    brdf_data, solar_zenith = SatBRDF.Sat_BRDF(ls_dc, ls_query, ls_sat_array, field_data)
    ls_ground_WSbrdf, dummy, hb, br = BRDF.ReadAndCalc(brdf_data, ls_ground_bands, s2_ground_bands, field_data)
    ls_ground_WSbrdf = FudgeGPS.fudge_gps(ls_ground_WSbrdf, Corners, RockWalk, StartCorner)
    return ls_sat_array, ls_sat_bigarray, s2_sat_array, s2_sat_bigarray, ls8_usgs_array, ls8_usgs_bigarray, \
           solar_zenith, ls_query, s2_query, ls_dc, s2_dc, ls_ground_WSbrdf
