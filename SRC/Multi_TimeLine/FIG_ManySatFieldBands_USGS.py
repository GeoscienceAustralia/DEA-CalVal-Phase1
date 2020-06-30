import matplotlib.pyplot as plt
import numpy as np


#
# Determine appropriate error bars for satellite data, based on the standard
# deviation of a Field-sized box, moved around the satellite bounding box.
#
def SDev(sat_array, satname):
    if satname == 'Landsat':
        satfieldpix = 4
    elif satname == 'Sentinel':
        satfieldpix = 10
    else:
        print('Sat name should be one of Landsat or Sentinel. I got', satname)

    SDeviation = []
    for k in sat_array.data_vars:
        if len(sat_array[k].x)+len(sat_array[k].y) > 2*satfieldpix:
            loost = []
            for i in range(len(sat_array[k].x)-satfieldpix-1):
                for j in range(len(sat_array[k].y)-satfieldpix-1):
                    loost.append(float(sat_array[k][0][i:i+satfieldpix, j:j+satfieldpix].mean()))
            SDeviation.append(np.std(loost)/10000)
        else:
            SDeviation.append(float(np.std(sat_array[k])/10000))
    return SDeviation

#
## Figure 
#
### Plot comparison spectra of INNER satellite and field data, on a
### pixel-by-pixel basis
#
# Error bars are shown for the field data, based on the standard deviation of
# the pixels within the field.
#
def FIG_many_sat_field_bands(ls8_array, ls8_usgs_array, fls8_df, fls8_usgs_df, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(6.5, 6.5))
    fig.suptitle(fig_title+': Satellite and Field data comparison by band', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    SDeviation = SDev(ls8_array, 'Landsat')

    ls8_means = [col for col in fls8_df.columns if 'ls8_mean' in col]
    ls8_stds = [col for col in fls8_df.columns if 'ls8_SD' in col]
    for i in range(len(ls8_means)):
        fls8_df.plot(y=ls8_means[i], ax=axes[0], legend=False)

    ls8_usgs_means = [col for col in fls8_usgs_df.columns if 'ls8_mean' in col]
    ls8_usgs_stds = [col for col in fls8_usgs_df.columns if 'ls8_SD' in col]
    for i in range(len(ls8_usgs_means)):
        fls8_usgs_df.plot(y=ls8_usgs_means[i], ax=axes[1], legend=False)

    axes[0].set_title('Landsat 8')
    axes[1].set_title('Landsat8 USGS')
    axes[0].set_ylabel('Reflectance')

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_InnerFieldBandCompare.png')
