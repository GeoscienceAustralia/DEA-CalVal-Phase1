import datacube
from datacube.utils import masking
from datacube.helpers import ga_pq_fuser

##
## Query Satellite data, based on manual input location and time
## INCLUDE CLOUD MASKS
##
#def create_long_arrays(ldc, sdc, lquery, squery, lquery2, squery2):
#
#    sb_names = ['nbart_coastal_aerosol', 'nbart_blue', 'nbart_green', 'nbart_red', 'nbart_red_edge_1', 'nbart_red_edge_2', 'nbart_red_edge_3', 'nbart_nir_1', 'nbart_nir_2', 'nbart_swir_2', 'nbart_swir_3', 'fmask']
#
#    temp = sdc.load(product='s2a_ard_granule', measurements=sb_names, **squery)
#    s2a_array = temp.where(temp.fmask==1)
#    temp = sdc.load(product='s2b_ard_granule', measurements=sb_names, **squery)
#    s2b_array = temp.where(temp.fmask==1)
#
#    temp = sdc.load(product='s2a_ard_granule', measurements=sb_names, **squery2)
#    s2a_bigarray = temp.where(temp.fmask==1)
#    temp = sdc.load(product='s2b_ard_granule', measurements=sb_names, **squery2)
#    s2b_bigarray = temp.where(temp.fmask==1)
#
#    ls8_temp = ldc.load(product='ga_ls8c_ard_3', **lquery)
#    ls8_bigtemp = ldc.load(product='ga_ls8c_ard_3', **lquery2)
#
#    ls8_pq = ldc.load(product='ls8_pq_scene', fuse_func=ga_pq_fuser, **lquery2)
#
#    good_quality = masking.make_mask(ls8_pq.pqa,
#                                 cloud_acca='no_cloud',
#                                 cloud_fmask='no_cloud',
#                                 cloud_shadow_acca='no_cloud_shadow',
#                                 cloud_shadow_fmask='no_cloud_shadow',
#                                 blue_saturated=False,
#                                 green_saturated=False,
#                                 red_saturated=False,
#                                 nir_saturated=False,
#                                 swir1_saturated=False,
#                                 swir2_saturated=False,
#                                 contiguous=True)
#    ls8_array = ls8_temp.where(good_quality)
#    ls8_bigarray = ls8_bigtemp.where(good_quality)
#
#    ls8_array = ls8_array.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'})
#    ls8_bigarray = ls8_bigarray.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'})
#
#    return ls8_array, s2a_array, s2b_array, ls8_bigarray, s2a_bigarray, s2b_bigarray

#
# Query Satellite data, based on manual input location and time
# NO CLOUD MASKS
#
def create_long_arrays_nomask(ldc, sdc, lquery, squery, lquery2, squery2):

    sb_names = ['nbart_coastal_aerosol', 'nbart_blue', 'nbart_green', 'nbart_red', 'nbart_red_edge_1', 'nbart_red_edge_2', 'nbart_red_edge_3', 'nbart_nir_1', 'nbart_nir_2', 'nbart_swir_2', 'nbart_swir_3', 'fmask']

    s2a_array = sdc.load(product='s2a_ard_granule', measurements=sb_names, dask_chunks={}, **squery)
    s2b_array = sdc.load(product='s2b_ard_granule', measurements=sb_names, dask_chunks={}, **squery)

    s2a_bigarray = sdc.load(product='s2a_ard_granule', measurements=sb_names, dask_chunks={}, **squery2)
    s2b_bigarray = sdc.load(product='s2b_ard_granule', measurements=sb_names, dask_chunks={}, **squery2)

    ls8_array = ldc.load(product='ga_ls8c_ard_3', dask_chunks={}, **lquery)
    ls8_bigarray = ldc.load(product='ga_ls8c_ard_3', dask_chunks={}, **lquery2)

    #ls8_array = ls8_array.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'})
    #ls8_bigarray = ls8_bigarray.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'})

    return ls8_array, s2a_array, s2b_array, ls8_bigarray, s2a_bigarray, s2b_bigarray
