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

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9.5, 9.5))
    fig.suptitle(fig_title+': Pixel by pixel comparison of field and satellite data', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    plt.xlim(plot_scale[0], plot_scale[1])
    plt.ylim(plot_scale[2], plot_scale[3])
    p1, p2 = [-1, 2], [-1, 2]
    plt.plot(p1, p2, marker='o')
    plt.xlabel('Field Reflectance per pixel')
    plt.ylabel('Satellite Reflectance per pixel')

    plt.scatter(field_array.coastal_aerosol[0]/10000, sat_array.coastal_aerosol[0]/10000, marker='o', facecolors='none', edgecolors='red')
    plt.scatter(field_array.blue[0]/10000, sat_array.blue[0]/10000, marker='^', facecolors='none', edgecolors='orange')
    plt.scatter(field_array.green[0]/10000, sat_array.green[0]/10000, marker='s', facecolors='none', edgecolors='yellow')
    plt.scatter(field_array.red[0]/10000, sat_array.red[0]/10000, marker='+', color='green')
    plt.scatter(field_array.nir[0]/10000, sat_array.nir[0]/10000, marker='x', color='blue')
    plt.scatter(field_array.swir1[0]/10000, sat_array.swir1[0]/10000, marker='D', facecolors='none', edgecolors='darkblue')
    plt.scatter(field_array.swir2[0]/10000, sat_array.swir2[0]/10000, marker='*', facecolors='none', edgecolors='black')

    x_stretch = (plot_scale[1]-plot_scale[0])
    y_stretch = (plot_scale[3]-plot_scale[2])

    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.950*y_stretch)+plot_scale[2], marker='o', facecolors='none', edgecolors='red')
    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.925*y_stretch)+plot_scale[2], marker='^', facecolors='none', edgecolors='orange')
    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.900*y_stretch)+plot_scale[2], marker='s', facecolors='none', edgecolors='yellow')
    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.875*y_stretch)+plot_scale[2], marker='+', color='green')
    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.850*y_stretch)+plot_scale[2], marker='x', color='blue')
    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.825*y_stretch)+plot_scale[2], marker='D', facecolors='none', edgecolors='darkblue')
    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.800*y_stretch)+plot_scale[2], marker='*', facecolors='none', edgecolors='black')

    plt.figtext(0.185, 0.895, "Band 1 - Coastal Aerosol")
    plt.figtext(0.185, 0.872, "Band 2 - Blue")
    plt.figtext(0.185, 0.850, "Band 3 - Green")
    plt.figtext(0.185, 0.830, "Band 4 - Red")
    plt.figtext(0.185, 0.809, "Band 5 - NIR")
    plt.figtext(0.185, 0.786, "Band 6 - SWIR1")
    plt.figtext(0.185, 0.766, "Band 7 - SWIR2")
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_PixelByPixelComparison.png')
