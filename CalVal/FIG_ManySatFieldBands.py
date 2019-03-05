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
def FIG_many_sat_field_bands(ls8_array, s2a_array, s2b_array, fls8_df, fs2a_df, fs2b_df, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(12.5, 6.5))
    fig.suptitle(fig_title+': Satellite and Field data comparison by band', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    #SDeviation = SDev(s2b_array, 'Sentinel')

    ls8_means = [col for col in fls8_df.columns if 'ls8_mean' in col]
    ls8_stds = [col for col in fls8_df.columns if 'ls8_SD' in col]
    for i in range(len(ls8_means)):
        fls8_df.plot(y=ls8_means[i], ax=axes[0], legend=False)

    s2a_means = [col for col in fs2a_df.columns if 'S2a_mean' in col]
    s2a_stds = [col for col in fs2a_df.columns if 'S2a_SD' in col]
    for i in range(len(s2a_means)):
        fs2a_df.plot(y=s2a_means[i], ax=axes[1], legend=False)

    s2b_means = [col for col in fs2b_df.columns if 'S2b_mean' in col]
    s2b_stds = [col for col in fs2b_df.columns if 'S2b_SD' in col]
    for i in range(len(s2b_means)):
        fs2b_df.plot(y=s2b_means[i], ax=axes[2], legend=False)

    axes[0].set_title('Landsat 8')
    axes[1].set_title('Sentinel 2a')
    axes[2].set_title('Sentinel 2b')
    axes[0].set_ylabel('Reflectance')

    #if field_data[3] == 'Landsat8':
    #    axes.set_xticklabels(['Band0','Band 1','Band 2','Band 3','Band 4','Band 5','Band 6', 'Band 7'])
#
#    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
#        axes.set_xticklabels(['Band 1','Band 2','Band 3','Band 4','Band 5','Band 6', 'Band 7', 'Band 8', 'Band 8a', 'Band 11', 'Band 12'])
#
#    else:
#        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_InnerFieldBandCompare.png')
