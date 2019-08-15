#!/usr/bin/env python

from pprint import pprint
from posixpath import join as ppjoin
import dateutil
import h5py
from shapely.geometry import Point, box
import geopandas
from wagl.brdf import get_brdf_data
from wagl.constants import DatasetName
from wagl.geobox import GriddedGeoBox
from wagl.hdf5 import read_h5_table, write_scalar
import numpy
from osgeo import osr
from affine import Affine

import json

BRDF = {'brdf_path': '/g/data/v10/eoancillarydata-2/BRDF/MCD43A1.006',
        'brdf_premodis_path': '/g/data/v10/eoancillarydata-2/BRDF_FALLBACK/MCD43A1.006',
        'ocean_mask_path': '/g/data/v10/eoancillarydata-2/ocean_mask/base_oz_tile_set_water_mask_geotif.tif'}

with open('sensors.json') as fl:
    SENSORS = json.load(fl)

def band_info(platform, instrument, alias):
    table = SENSORS[platform][instrument]["band_ids"]

    for key, value in table.items():
        if value['alias'] == alias:
            return value


class MimicAcquisition(object):

    def __init__(self, band_data):

        self.no_data = 0

        self.acquisition_datetime = dateutil.parser.parse('2018-02-12 01:07:03')
        self.brdf_datasets = band_data['brdf_datasets']

        bbox = geopandas.GeoDataFrame({'geometry': [box(149.46124666666665, -35.092625, 149.46245833333333, -35.09139666666667)]})
        bbox.crs = {'init': 'EPSG:4326'}
        albers = bbox.to_crs(epsg=3577)
        buff = albers.buffer(1000)
        lonlat = buff.to_crs(epsg=4326)

        minx, miny, maxx, maxy = lonlat.total_bounds

        self.geobox = GriddedGeoBox(shape=(1, 1), origin=(minx, miny), pixelsize=(maxx - minx, maxy - miny), crs='EPSG:4326')

    def gridded_geo_box(self):
        return self.geobox

    def data(self):
        return numpy.array([[1]])


if __name__ == "__main__":
    platform = "SENTINEL_2A"
    instrument = "MSI"
    alias = ["Coastal-Aerosol", "Blue", "Green", "Red", "Red-Edge-1", "Red-Edge-2", "Red-Edge-3", "NIR-1", "NIR-2",
             "SWIR-2", "SWIR-3"]
   
    for alias in alias:
        acq_mimic = MimicAcquisition(band_info(platform, instrument, alias))
        
        brdf_data = get_brdf_data(acq_mimic, BRDF)
        
        print(' '.join(str(d['value']) for d in brdf_data.values()))
