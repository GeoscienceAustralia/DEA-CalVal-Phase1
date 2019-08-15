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
        'brdf_fallback_path': '/g/data/v10/eoancillarydata-2/BRDF_FALLBACK/MCD43A1.006',
        'ocean_mask_path': '/g/data/v10/eoancillarydata-2/ocean_mask/base_oz_tile_set_water_mask_geotif.tif'}

with open('sensors.json') as fl:
    SENSORS = json.load(fl)

def band_info(platform, instrument, band_name):
    table = SENSORS[platform][instrument]["band_ids"]

    for key, value in table.items():
        if value['band_name'] == band_name:
            return value


class MimicAcquisition(object):

    def __init__(self, band_data):

        self.no_data = 0

        self.acquisition_datetime = dateutil.parser.parse('2018-06-21 00:11:45')
        self.brdf_datasets = band_data['brdf_datasets']

        bbox = geopandas.GeoDataFrame({'geometry': [box(142.93854167, -22.527813889, 142.93854167, -22.527813889)]})
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
    band_name = ['BAND-1', 'BAND-2', 'BAND-3', 'BAND-4', 'BAND-5', 'BAND-6', 'BAND-7', 'BAND-8', 'BAND-8A',
                 'BAND-11', 'BAND-12'] 
    #alias = ["Coastal-Aerosol", "Blue", "Green", "Red", "Red-Edge-1", "Red-Edge-2", "Red-Edge-3", "NIR-1", "NIR-2",
    #         "SWIR-2", "SWIR-3"]
   
    for band_name in band_name:
        acq_mimic = MimicAcquisition(band_info(platform, instrument, band_name))
        
        brdf_data = get_brdf_data(acq_mimic, BRDF)
        
        print(platform, band_name.lower().replace('-', ''), '1', ' '.join(str(d['value']) for d in brdf_data.values()))
