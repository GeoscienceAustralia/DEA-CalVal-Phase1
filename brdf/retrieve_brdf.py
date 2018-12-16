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

FNAME = 'sample-tables.h5'
BRDF_PATH = '/g/data/u39/public/data/modis/lpdaac-mosaics-cmar/v1-hdf4/aust/MCD43A1.005'
BRDF_PREMODIS_PATH = '/g/data/v10/eoancillarydata/brdf-jl/data'


class MimicGeobox(object):

    def __init__(self, extent):

        self.ul_lonlat = (extent[0], extent[-1])
        self.lr_lonlat = (extent[2], extent[1])


class MimicAcquisition(object):

    def __init__(self, h5_group, dataset_name):

        dset = h5_group[dataset_name]
        self._group = h5_group
        self._pathname = dataset_name

        setattr(self, 'acquisition_datetime', dateutil.parser.parse('2018-05-07 23:57:35'))
        setattr(self, 'brdf_wavelength', dset.attrs['brdf_wavelength'])

        bbox = geopandas.GeoDataFrame({'geometry': [box(142.93854167, -22.527813889, 142.93854167, -22.527813889)]})
        bbox.crs = {'init': 'EPSG:4326'}
        albers = bbox.to_crs(epsg=3577)
        buff = albers.buffer(1000)
        lonlat = buff.to_crs(epsg=4326)

        self.buffered_extent = lonlat.total_bounds

    def gridded_geo_box(self):
        return MimicGeobox(self.buffered_extent)


if __name__ == "__main__":

    with h5py.File(FNAME, 'r') as fid:
        for platform in fid:
            for name in fid[platform]:
                acq_mimic = MimicAcquisition(fid[platform], name)

                brdf_data = get_brdf_data(acq_mimic, BRDF_PATH, BRDF_PREMODIS_PATH)

                count=0
                sval=[0,0,0]
                for param in brdf_data:
                    value = brdf_data[param].pop('value')
                    sval[count] = value
                    count+=1
                print(platform, name.lower().replace('-', ''), ' '.join( str(e) for e in sval ) )
