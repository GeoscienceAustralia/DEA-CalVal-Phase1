from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import csv, glob, sys, os, re, shutil
import math
import pyproj

import datacube
import DEAPlotting
import matplotlib.pyplot as plt


#
# # Figure 
#
### Comparison plot of Field and satellite data
#
# Plot shows a pixel-by-pixel comparison of all pixels where field data exists.
# Different band data are shown in different colours and different symbols.
#
def FIG_sat_field_scatter_compare(sat_array, field_array, plot_scale, output, field_data, fignum):

    #fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(6.0, 6.0))
    #fig.suptitle(fig_title+':\nPixel by pixel comparison of field and satellite data', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    plt.xlim(plot_scale[0], plot_scale[1])
    plt.ylim(plot_scale[2], plot_scale[3])
    p1, p2 = [-1, 2], [-1, 2]
    plt.plot(p1, p2, marker='o')
    plt.xlabel('Field Reflectance per pixel', fontweight='bold')
    plt.ylabel('Satellite Reflectance per pixel', fontweight='bold')

    if field_data[3] == 'Landsat8':
        plt.scatter(field_array.coastal_aerosol[0]/10000, sat_array.coastal_aerosol[0]/10000, marker='o', facecolors='none', edgecolors='red')
        plt.scatter(field_array.blue[0]/10000, sat_array.blue[0]/10000, marker='^', facecolors='none', edgecolors='orange')
        plt.scatter(field_array.green[0]/10000, sat_array.green[0]/10000, marker='s', facecolors='none', edgecolors='yellow')
        plt.scatter(field_array.red[0]/10000, sat_array.red[0]/10000, marker='+', color='green')
        plt.scatter(field_array.nir[0]/10000, sat_array.nir[0]/10000, marker='x', color='blue')
        plt.scatter(field_array.swir1[0]/10000, sat_array.swir1[0]/10000, marker='D', facecolors='none', edgecolors='darkblue')
        plt.scatter(field_array.swir2[0]/10000, sat_array.swir2[0]/10000, marker='*', facecolors='none', edgecolors='black')

    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        plt.scatter(field_array.nbart_coastal_aerosol[0]/10000, sat_array.nbart_coastal_aerosol[0]/10000, marker='o', facecolors='none', edgecolors='red')
        plt.scatter(field_array.nbart_blue[0]/10000, sat_array.nbart_blue[0]/10000, marker='^', facecolors='none', edgecolors='orange')
        plt.scatter(field_array.nbart_green[0]/10000, sat_array.nbart_green[0]/10000, marker='s', facecolors='none', edgecolors='yellow')
        plt.scatter(field_array.nbart_red[0]/10000, sat_array.nbart_red[0]/10000, marker='+', color='green')
        plt.scatter(field_array.nbart_red_edge_1[0]/10000, sat_array.nbart_red_edge_1[0]/10000, marker='+', color='blue')
        plt.scatter(field_array.nbart_red_edge_2[0]/10000, sat_array.nbart_red_edge_2[0]/10000, marker='+', color='orange')
        plt.scatter(field_array.nbart_red_edge_3[0]/10000, sat_array.nbart_red_edge_3[0]/10000, marker='+', color='red')
        plt.scatter(field_array.nbart_nir_1[0]/10000, sat_array.nbart_nir_1[0]/10000, marker='x', color='blue')
        plt.scatter(field_array.nbart_nir_2[0]/10000, sat_array.nbart_nir_2[0]/10000, marker='x', color='yellow')
        plt.scatter(field_array.nbart_swir_2[0]/10000, sat_array.nbart_swir_2[0]/10000, marker='D', facecolors='none', edgecolors='darkblue')
        plt.scatter(field_array.nbart_swir_3[0]/10000, sat_array.nbart_swir_3[0]/10000, marker='*', facecolors='none', edgecolors='black')
    
    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    x_stretch = (plot_scale[1]-plot_scale[0])
    y_stretch = (plot_scale[3]-plot_scale[2])

    if field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.975*y_stretch)+plot_scale[2], marker='o', facecolors='none', edgecolors='red')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.945*y_stretch)+plot_scale[2], marker='^', facecolors='none', edgecolors='orange')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.915*y_stretch)+plot_scale[2], marker='s', facecolors='none', edgecolors='yellow')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.885*y_stretch)+plot_scale[2], marker='+', color='green')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.855*y_stretch)+plot_scale[2], marker='+', color='blue')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.823*y_stretch)+plot_scale[2], marker='+', color='orange')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.793*y_stretch)+plot_scale[2], marker='+', color='red')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.762*y_stretch)+plot_scale[2], marker='x', color='blue')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.731*y_stretch)+plot_scale[2], marker='x', color='yellow')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.698*y_stretch)+plot_scale[2], marker='D', facecolors='none', edgecolors='darkblue')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.665*y_stretch)+plot_scale[2], marker='*', facecolors='none', edgecolors='black')
    
        plt.figtext(0.178, 0.874, "Band 1 - Coastal Aerosol")
        plt.figtext(0.178, 0.852, "Band 2 - Blue")
        plt.figtext(0.178, 0.827, "Band 3 - Green")
        plt.figtext(0.178, 0.805, "Band 4 - Red")
        plt.figtext(0.178, 0.782, "Band 5 - Red Edge 1")
        plt.figtext(0.178, 0.759, "Band 6 - Red Edge 2")
        plt.figtext(0.178, 0.734, "Band 7 - Red Edge 3")
        plt.figtext(0.178, 0.711, "Band 8 - NIR")
        plt.figtext(0.178, 0.686, "Band 8a - Narrow NIR")
        plt.figtext(0.178, 0.661, "Band 11 - SWIR 2")
        plt.figtext(0.178, 0.636, "Band 12 - SWIR 3")

    elif field_data[3] == 'Landsat8':
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.975*y_stretch)+plot_scale[2], marker='o', facecolors='none', edgecolors='red')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.945*y_stretch)+plot_scale[2], marker='^', facecolors='none', edgecolors='orange')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.915*y_stretch)+plot_scale[2], marker='s', facecolors='none', edgecolors='yellow')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.885*y_stretch)+plot_scale[2], marker='+', color='green')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.855*y_stretch)+plot_scale[2], marker='x', color='blue')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.825*y_stretch)+plot_scale[2], marker='D', facecolors='none', edgecolors='darkblue')
        plt.scatter((0.03*x_stretch)+plot_scale[0], (0.795*y_stretch)+plot_scale[2], marker='*', facecolors='none', edgecolors='black')
    
        plt.figtext(0.178, 0.885, "Band 1 - Coastal Aerosol")
        plt.figtext(0.178, 0.860, "Band 2 - Blue")
        plt.figtext(0.178, 0.835, "Band 3 - Green")
        plt.figtext(0.178, 0.812, "Band 4 - Red")
        plt.figtext(0.178, 0.787, "Band 5 - NIR")
        plt.figtext(0.178, 0.763, "Band 6 - SWIR1")
        plt.figtext(0.178, 0.738, "Band 7 - SWIR2")

    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_PixelByPixelComparison.png', dpi=300)
