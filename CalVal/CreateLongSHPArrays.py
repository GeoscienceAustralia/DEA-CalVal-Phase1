import math
import pandas as pd
import fiona
import rasterio.features

import datacube
from datacube.storage import masking
from datacube.helpers import ga_pq_fuser
from datacube.utils import geometry


def geometry_mask(geoms, geobox, all_touched=False, invert=False):
    """
    Create a mask from shapes.

    By default, mask is intended for use as a
    numpy mask, where pixels that overlap shapes are False.
    :param list[Geometry] geoms: geometries to be rasterized
    :param datacube.utils.GeoBox geobox:
    :param bool all_touched: If True, all pixels touched by geometries will be burned in. If
                             false, only pixels whose center is within the polygon or that
                             are selected by Bresenham's line algorithm will be burned in.
    :param bool invert: If True, mask will be True for pixels that overlap shapes.
    """
    return rasterio.features.geometry_mask([geom.to_crs(geobox.crs) for geom in geoms],
                                           out_shape=geobox.shape,
                                           transform=geobox.affine,
                                           all_touched=all_touched,
                                           invert=invert)


def feature_from_shapefile(filename, feature_id):

    with fiona.open(filename) as fl:
        for feature in fl:
            # could check for feature['properties']['id']
            # or feature['properties']['ID'] as well
            # depending on the file
            if feature_id == feature['id']:
                return feature
    raise ValueError('{} not found in {}'.format(feature_id, filename))


def create_long_SHP_arrays(shape_file, feature_id):

    feature = feature_from_shapefile(shape_file, feature_id)

    with fiona.open(shape_file) as shapes:
        crs = geometry.CRS(shapes.crs_wkt)
    
    geom = geometry.Geometry(feature['geometry'], crs=crs)


    dc = datacube.Datacube()

    query = {
             'time': ('2013-01-01', '2118-12-31'),
             'geopolygon': geom,
             'output_crs': 'EPSG:3577',
             'resampling': 'bilinear',
             'group_by': 'solar_day',
            }

    sb_names = ['nbart_coastal_aerosol', 'nbart_blue', 'nbart_green', 'nbart_red', 'nbart_red_edge_1', 'nbart_red_edge_2', 'nbart_red_edge_3', 'nbart_nir_1', 'nbart_nir_2', 'nbart_swir_2', 'nbart_swir_3', 'fmask']

    s2a_array = dc.load(product='s2a_ard_granule', measurements=sb_names, resolution=(-10, 10), **query)
    s2b_array = dc.load(product='s2b_ard_granule', measurements=sb_names, resolution=(-10, 10), **query)

    ls8_array = dc.load(product='ls8_nbart_scene', resolution=(-25, 25), **query)

    ls8_array = ls8_array.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'})

    lmask = geometry_mask([geom], ls8_array.geobox, invert=True)
    ls8_array = ls8_array.where(lmask)

    smask = geometry_mask([geom], s2a_array.geobox, invert=True)
    s2a_array = s2a_array.where(smask)
    s2b_array = s2b_array.where(smask)

    return ls8_array, s2a_array, s2b_array
