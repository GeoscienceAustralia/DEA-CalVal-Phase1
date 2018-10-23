import datacube
from datacube.storage import masking
from datacube.helpers import ga_pq_fuser

#
# Query Satellite data, based on manual input location and time
# INCLUDE CLOUD MASKS
#
def create_long_arrays(ldc, udc, lquery, lquery2):

    usgs_names = ['coastal_aerosol', 'blue', 'green', 'red', 'nir', 'swir1', 'swir2']

    ls8_temp = ldc.load(product='ls8_nbart_scene', **lquery)
    ls8_bigtemp = ldc.load(product='ls8_nbart_scene', **lquery2)

    ls8_usgs_temp = udc.load(product='ls8_usgs_l2c1', measurements=usgs_names, **lquery)
    ls8_usgs_bigtemp = udc.load(product='ls8_usgs_l2c1', measurements=usgs_names, **lquery2)

    ls8_pq = ldc.load(product='ls8_pq_scene', fuse_func=ga_pq_fuser, **lquery2)

    good_quality = masking.make_mask(ls8_pq.pqa,
                                 cloud_acca='no_cloud',
                                 cloud_fmask='no_cloud',
                                 cloud_shadow_acca='no_cloud_shadow',
                                 cloud_shadow_fmask='no_cloud_shadow',
                                 blue_saturated=False,
                                 green_saturated=False,
                                 red_saturated=False,
                                 nir_saturated=False,
                                 swir1_saturated=False,
                                 swir2_saturated=False,
                                 contiguous=True)
    ls8_array = ls8_temp.where(good_quality)
    ls8_bigarray = ls8_bigtemp.where(good_quality)

    ls8_usgs_array = ls8_usgs_temp.where(good_quality)
    ls8_usgs_bigarray = ls8_usgs_bigtemp.where(good_quality)

    ls8_array.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'}, inplace=True)
    ls8_bigarray.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'}, inplace=True)

    return ls8_array, ls8_usgs_array, ls8_bigarray, ls8_usgs_bigarray
#
# Query Satellite data, based on manual input location and time
# NO CLOUD MASKS
#
def create_long_arrays_nomask(ldc, udc, lquery, lquery2):

    usgs_names = ['coastal_aerosol', 'blue', 'green', 'red', 'nir', 'swir1', 'swir2']

    ls8_array = ldc.load(product='ls8_nbart_scene', **lquery)
    ls8_bigarray = ldc.load(product='ls8_nbart_scene', **lquery2)

    ls8_usgs_array = udc.load(product='ls8_usgs_l2c1', measurements=usgs_names, **lquery)
    ls8_usgs_bigarray = udc.load(product='ls8_usgs_l2c1', measurements=usgs_names, **lquery2)

    ls8_array.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'}, inplace=True)
    ls8_bigarray.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'}, inplace=True)

    return ls8_array, ls8_usgs_array, ls8_bigarray, ls8_usgs_bigarray
