#!/usr/bin/env python

from pprint import pprint
from posixpath import join as ppjoin
import dateutil
import h5py
from shapely.geometry import Point, box
import geopandas
from wagl.brdf import get_brdf_data
from wagl.constants import DatasetName
from wagl.hdf5 import read_h5_table, write_scalar
import numpy
from osgeo import osr
from affine import Affine

FNAME = 'sample-tables.h5'
BRDF = {'brdf_path': '/g/data/v10/eoancillarydata-2/BRDF/MCD43A1.006',
        'brdf_premodis_path': '/g/data/v10/eoancillarydata-2/BRDF_FALLBACK/MCD43A1.006',
        'ocean_mask_path': '/g/data/v10/eoancillarydata-2/ocean_mask/base_oz_tile_set_water_mask_geotif.tif'}


class MimicGeobox(object):

    def __init__(self, extent):
        minx, miny, maxx, maxy = extent

        self.ul_lonlat = (minx, maxy)
        self.lr_lonlat = (maxx, miny)
        self.crs = osr.SpatialReference()
        self.crs.ImportFromEPSG(4326)
        self.transform = Affine(maxx - minx, 0, minx, 0, maxy - miny, miny)


class MimicAcquisition(object):

    def __init__(self, h5_group, dataset_name):

        dset = h5_group[dataset_name]
        self._group = h5_group
        self._pathname = dataset_name
        self.no_data = 0

        setattr(self, 'acquisition_datetime', dateutil.parser.parse('2018-02-12 01:07:03'))
        setattr(self, 'brdf_wavelength', dset.attrs['brdf_wavelength'])

        bbox = geopandas.GeoDataFrame({'geometry': [box(149.46124666666665, -35.092625, 149.46245833333333, -35.09139666666667)]})
        bbox.crs = {'init': 'EPSG:4326'}
        albers = bbox.to_crs(epsg=3577)
        buff = albers.buffer(1000)
        lonlat = buff.to_crs(epsg=4326)

        self.buffered_extent = lonlat.total_bounds

    def gridded_geo_box(self):
        return MimicGeobox(self.buffered_extent)

    def data(self):
        return numpy.array([0])


if __name__ == "__main__":

    with h5py.File(FNAME, 'r') as fid:
        for platform in fid:
            for name in fid[platform]:
                acq_mimic = MimicAcquisition(fid[platform], name)

                brdf_data = get_brdf_data(acq_mimic, BRDF)

                count=0
                sval=[0,0,0]
                for param in brdf_data:
                    value = brdf_data[param].pop('value')
                    sval[count] = value
                    count+=1
                print(platform, name.lower().replace('-', ''), ' '.join( str(e) for e in sval ) )
