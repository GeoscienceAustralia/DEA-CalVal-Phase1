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
# Plot shows an averaged comparison of all pixels where field data exists.
# Different band data are shown in different colours and different symbols.
#
def FIG_sat_field_avg_scatter_compare(sat_array, field_array, plot_scale, fstat_df, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9.5, 9.5))
    fig.suptitle(fig_title+': Averaged comparison of field and satellite data', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    plt.xlim(plot_scale[0], plot_scale[1])
    plt.ylim(plot_scale[2], plot_scale[3])
    p1, p2 = [-1, 2], [-1, 2]
    plt.plot(p1, p2, marker='o')
    plt.xlabel('Field Reflectance per pixel')
    plt.ylabel('Satellite Reflectance per pixel')

    if field_data[3] == 'Landsat8':
        plt.errorbar(x=field_array.coastal_aerosol[0].mean()/10000, y=sat_array.coastal_aerosol[0].mean()/10000, xerr=fstat_df.Field_SD['Band1'], yerr=fstat_df.Sat_SD['Band1'], fmt='o', mfc='white', mec='red', color='red', capsize=3)
        plt.errorbar(x=field_array.blue[0].mean()/10000, y=sat_array.blue[0].mean()/10000, xerr=fstat_df.Field_SD['Band2'], yerr=fstat_df.Sat_SD['Band2'], fmt='^', mfc='white', mec='orange', color='orange', capsize=3)
        plt.errorbar(x=field_array.green[0].mean()/10000, y=sat_array.green[0].mean()/10000, xerr=fstat_df.Field_SD['Band3'], yerr=fstat_df.Sat_SD['Band3'], fmt='s', mfc='white', mec='yellow', color='yellow', capsize=3)
        plt.errorbar(x=field_array.red[0].mean()/10000, y=sat_array.red[0].mean()/10000, xerr=fstat_df.Field_SD['Band4'], yerr=fstat_df.Sat_SD['Band4'], fmt='+', mfc='white', mec='green', color='green', capsize=3)
        plt.errorbar(x=field_array.nir[0].mean()/10000, y=sat_array.nir[0].mean()/10000, xerr=fstat_df.Field_SD['Band5'], yerr=fstat_df.Sat_SD['Band5'], fmt='x', mfc='white', mec='blue', color='blue', capsize=3)
        plt.errorbar(x=field_array.swir1[0].mean()/10000, y=sat_array.swir1[0].mean()/10000, xerr=fstat_df.Field_SD['Band6'], yerr=fstat_df.Sat_SD['Band6'], fmt='D', mfc='white', mec='darkblue', color='darkblue', capsize=3)
        plt.errorbar(x=field_array.swir2[0].mean()/10000, y=sat_array.swir2[0].mean()/10000, xerr=fstat_df.Field_SD['Band7'], yerr=fstat_df.Sat_SD['Band7'], fmt='*', mfc='white', mec='black', color='black', capsize=3)
        
    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        plt.errorbar(x=field_array.nbart_coastal_aerosol[0].mean()/10000, y=sat_array.nbart_coastal_aerosol[0].mean()/10000, xerr=fstat_df.Field_SD['Band1'], yerr=fstat_df.Sat_SD['Band1'], fmt='o', color='red', mfc='white', mec='red', capsize=3)
        plt.errorbar(x=field_array.nbart_blue[0].mean()/10000, y=sat_array.nbart_blue[0].mean()/10000, xerr=fstat_df.Field_SD['Band2'], yerr=fstat_df.Sat_SD['Band2'], fmt='^', color='orange', mfc='white', mec='orange', capsize=3)
        plt.errorbar(x=field_array.nbart_green[0].mean()/10000, y=sat_array.nbart_green[0].mean()/10000, xerr=fstat_df.Field_SD['Band3'], yerr=fstat_df.Sat_SD['Band3'], fmt='s', color='yellow', mfc='white', mec='yellow', capsize=3)
        plt.errorbar(x=field_array.nbart_red[0].mean()/10000, y=sat_array.nbart_red[0].mean()/10000, xerr=fstat_df.Field_SD['Band4'], yerr=fstat_df.Sat_SD['Band4'], fmt='+', color='green', mfc='white', mec='green', capsize=3)
        plt.errorbar(x=field_array.nbart_red_edge_1[0].mean()/10000, y=sat_array.nbart_red_edge_1[0].mean()/10000, xerr=fstat_df.Field_SD['Band5'], yerr=fstat_df.Sat_SD['Band5'], fmt='+', color='blue', mfc='white', mec='blue', capsize=3)
        plt.errorbar(x=field_array.nbart_red_edge_2[0].mean()/10000, y=sat_array.nbart_red_edge_2[0].mean()/10000, xerr=fstat_df.Field_SD['Band6'], yerr=fstat_df.Sat_SD['Band6'], fmt='+', color='orange', mfc='white', mec='orange', capsize=3)
        plt.errorbar(x=field_array.nbart_red_edge_3[0].mean()/10000, y=sat_array.nbart_red_edge_3[0].mean()/10000, xerr=fstat_df.Field_SD['Band7'], yerr=fstat_df.Sat_SD['Band7'], fmt='+', color='red', mfc='white', mec='red', capsize=3)
        plt.errorbar(x=field_array.nbart_nir_1[0].mean()/10000, y=sat_array.nbart_nir_1[0].mean()/10000, xerr=fstat_df.Field_SD['Band8'], yerr=fstat_df.Sat_SD['Band8'], fmt='x', color='blue', mfc='white', mec='blue', capsize=3)
        plt.errorbar(x=field_array.nbart_nir_2[0].mean()/10000, y=sat_array.nbart_nir_2[0].mean()/10000, xerr=fstat_df.Field_SD['Band8a'], yerr=fstat_df.Sat_SD['Band8a'], fmt='x', color='yellow', mfc='white', mec='yellow', capsize=3)
        plt.errorbar(x=field_array.nbart_swir_2[0].mean()/10000, y=sat_array.nbart_swir_2[0].mean()/10000, xerr=fstat_df.Field_SD['Band11'], yerr=fstat_df.Sat_SD['Band11'], fmt='D', color='darkblue', mfc='white', mec='darkblue', capsize=3)
        plt.errorbar(x=field_array.nbart_swir_3[0].mean()/10000, y=sat_array.nbart_swir_3[0].mean()/10000, xerr=fstat_df.Field_SD['Band12'], yerr=fstat_df.Sat_SD['Band12'], fmt='*', color='black', mfc='white', mec='black', capsize=3)
    
    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    x_stretch = (plot_scale[1]-plot_scale[0])
    y_stretch = (plot_scale[3]-plot_scale[2])

    if field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        plt.scatter((0.1*x_stretch)+plot_scale[0], (0.950*y_stretch)+plot_scale[2], marker='o', facecolors='none', edgecolors='red')
        plt.scatter((0.1*x_stretch)+plot_scale[0], (0.925*y_stretch)+plot_scale[2], marker='^', facecolors='none', edgecolors='orange')
        plt.scatter((0.1*x_stretch)+plot_scale[0], (0.900*y_stretch)+plot_scale[2], marker='s', facecolors='none', edgecolors='yellow')
        plt.scatter((0.1*x_stretch)+plot_scale[0], (0.875*y_stretch)+plot_scale[2], marker='+', color='green')
        plt.scatter((0.1*x_stretch)+plot_scale[0], (0.850*y_stretch)+plot_scale[2], marker='+', color='blue')
        plt.scatter((0.1*x_stretch)+plot_scale[0], (0.825*y_stretch)+plot_scale[2], marker='+', color='orange')
        plt.scatter((0.1*x_stretch)+plot_scale[0], (0.800*y_stretch)+plot_scale[2], marker='+', color='red')
        plt.scatter((0.1*x_stretch)+plot_scale[0], (0.775*y_stretch)+plot_scale[2], marker='x', color='blue')
        plt.scatter((0.1*x_stretch)+plot_scale[0], (0.750*y_stretch)+plot_scale[2], marker='x', color='yellow')
        plt.scatter((0.1*x_stretch)+plot_scale[0], (0.725*y_stretch)+plot_scale[2], marker='D', facecolors='none', edgecolors='darkblue')
        plt.scatter((0.1*x_stretch)+plot_scale[0], (0.700*y_stretch)+plot_scale[2], marker='*', facecolors='none', edgecolors='black')
    
        plt.figtext(0.185, 0.895, "Band 1 - Coastal Aerosol")
        plt.figtext(0.185, 0.872, "Band 2 - Blue")
        plt.figtext(0.185, 0.850, "Band 3 - Green")
        plt.figtext(0.185, 0.830, "Band 4 - Red")
        plt.figtext(0.185, 0.809, "Band 5 - Red Edge 1")
        plt.figtext(0.185, 0.786, "Band 6 - Red Edge 2")
        plt.figtext(0.185, 0.766, "Band 7 - Red Edge 3")
        plt.figtext(0.185, 0.744, "Band 8 - NIR")
        plt.figtext(0.185, 0.722, "Band 8a - Narrow IR")
        plt.figtext(0.185, 0.700, "Band 11 - SWIR 2")
        plt.figtext(0.185, 0.678, "Band 12 - SWIR 3")

    elif field_data[3] == 'Landsat8':
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

    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_AvgComparison.png')
