import matplotlib.pyplot as plt


#
## Figure 
#
### Plot satellite band extents against median ground spectrum
#
# This plot will show where the satellite bands fall, with respect to the
# spectrum and in particular, with respect to the atmospheric absorbtion features.
#
def FIG_band_extents(all_refls, band_min, band_max, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9.5, 6.5))
    #fig.suptitle(fig_title+': \nMedian ground reflectance with '+field_data[3]+' Bands shown as black bars', fontweight='bold')
    axes.set_ylabel("Surface Reflectance")
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    med = all_refls.median(axis=1)
    all_refls['Median'] = med
    all_refls.plot(y='Median', ax=axes, legend=False)

    if field_data[3] == 'Landsat8': 
        y_cord = [0.065, 0.075, 0.08, 0.09, 0.11, 0.18, 0.15, 0.12]
    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        y_cord = [0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.17, 0.15]
    else:
        print("Incorrect Satellite name - must be one of Landsat8 or Sentinel")

    for i in range(len(band_min)):
        plt.annotate('', xy = (band_min[i], y_cord[i]),  xycoords = 'data', \
            xytext = (band_max[i], y_cord[i]), textcoords = 'data',\
            arrowprops=dict(edgecolor='black', arrowstyle = '|-|, widthA=0.3, widthB=0.3'))
        plt.text((band_max[i]+band_min[i]-35)/2, y_cord[i]+0.002, i+1, fontsize=8)

    axes.set_xlabel("Wavelength (nm)")

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_BandWavelengths.png')
