import matplotlib.pyplot as plt
import numpy as np


#
# Determine appropriate error bars for satellite data, based on the standard
# deviation of a Field-sized box, moved around the satellite bounding box.
#
def SDev(sat_array, field_data):
    if field_data[3] == 'Landsat8':
        satfieldpix = 4
    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        satfieldpix = 10
    else:
        print('Sat name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

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
def FIG_SUB_sat_field_bands(sat_array, fstat_df, finner_df, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9.5, 9.5))
    fig.suptitle(fig_title+': Satellite and Field data comparison by band for inner pixels', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    SDeviation = SDev(sat_array, field_data)

    fstat_df.plot(y='Sat_mean', ax=axes, color='black')
    plt.errorbar(x=fstat_df.index, y=fstat_df['Sat_mean'], yerr=fstat_df['Sat_SD'], color='black', capsize=3)

    finner_df.plot(y='Sat_inner_mean', ax=axes, color='orange')
    finner_df.plot(y='Field_inner_mean', ax=axes, color='blue')
    axes.set_ylabel('Reflectance')
    axes.set_xlim(-0.5,len(fstat_df.index)-0.5)
    plt.errorbar(x=finner_df.index, y=finner_df['Field_inner_mean'], yerr=finner_df['Field_SD'], color='blue', capsize=3)

    if field_data[3] == 'Landsat8':
        axes.set_xticklabels(['Band 1','Band 2','Band 3','Band 4','Band 5','Band 6', 'Band 7',''])

    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        axes.set_xticklabels(['Band 1','Band 2','Band 3','Band 4','Band 5','Band 6', 'Band 7', 'Band 8', 'Band 8a', 'Band 11', 'Band 12'])

    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_InnerFieldBandCompare.png')
