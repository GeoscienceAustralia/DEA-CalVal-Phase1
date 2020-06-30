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
def FIG_sat_field_bands(sat_array, fstat_df, finner_df, output, field_data, fignum):

    #fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(3.5, 3.5))
    #fig.suptitle(fig_title+': Satellite and Field data comparison by band for inner pixels', fontweight='bold')
    plt.tight_layout(pad=2.7, w_pad=1.0, h_pad=1.0)

    SDeviation = SDev(sat_array, field_data)

    if field_data[3] == 'Landsat8':
        axes.set_xticklabels(['1','2','3','4','5','6', '7'])
        fid = finner_df.rename(index={'Band1': '1', 'Band2': '2', 'Band3': '3', 'Band4': '4', 'Band5': '5', 'Band6': '6', 'Band7': '7'},
                         columns={'Field_inner_mean': 'Field'})
        fsd = fstat_df.rename(index={'Band1': '1', 'Band2': '2', 'Band3': '3', 'Band4': '4', 'Band5': '5', 'Band6': '6', 'Band7': '7'},
                        columns={'Sat_mean': 'Landsat 8'})
        fsd.plot(y='Landsat 8', ax=axes, color='blue', linewidth=0.7)
        plt.errorbar(x=fsd.index, y=fsd['Landsat 8'], yerr=fsd['Sat_SD'], color='blue', capsize=3, linewidth=0.7)


    elif field_data[3] == 'Sentinel2a':
        axes.set_xticklabels(['1','2','3','4','5','6', '7', '8', '8a', '11', '12'])
        fid = fstat_df.rename(index={'Band1': '1', 'Band2': '2', 'Band3': '3', 'Band4': '4', 'Band5': '5', 'Band6': '6', 'Band7': '7',
                               'Band8': '8', 'Band8a': '8a', 'Band11': '11', 'Band12': '12'},
                        columns={'Field_mean': 'Field', 'Sat_mean': 'Sentinel 2a'})
        fsd = finner_df.rename(index={'Band1': '1', 'Band2': '2', 'Band3': '3', 'Band4': '4', 'Band5': '5', 'Band6': '6', 'Band7': '7',
                                'Band8': '8', 'Band8a': '8a', 'Band11': '11', 'Band12': '12'},
                         columns={'Field_inner_mean': 'Field', 'Sat_inner_mean': 'Sentinel 2a'})
        fsd.plot(y='Sentinel 2a', ax=axes, color='blue', linewidth=0.7)
        plt.errorbar(x=fsd.index, y=fsd['Sentinel 2a'], yerr=fsd['Sat_SD'], color='blue', capsize=3, linewidth=0.7)


    elif field_data[3] == 'Sentinel2b':
        axes.set_xticklabels(['1','2','3','4','5','6', '7', '8', '8a', '11', '12'])
        fid = fstat_df.rename(index={'Band1': '1', 'Band2': '2', 'Band3': '3', 'Band4': '4', 'Band5': '5', 'Band6': '6', 'Band7': '7',
                               'Band8': '8', 'Band8a': '8a', 'Band11': '11', 'Band12': '12'},
                        columns={'Field_mean': 'Field', 'Sat_mean': 'Sentinel 2b'})
        fsd = finner_df.rename(index={'Band1': '1', 'Band2': '2', 'Band3': '3', 'Band4': '4', 'Band5': '5', 'Band6': '6', 'Band7': '7',
                                'Band8': '8', 'Band8a': '8a', 'Band11': '11', 'Band12': '12'},
                         columns={'Field_inner_mean': 'Field', 'Sat_inner_mean': 'Sentinel 2b'})
        fsd.plot(y='Sentinel 2b', ax=axes, color='blue', linewidth=0.7)
        plt.errorbar(x=fsd.index, y=fsd['Sentinel 2b'], yerr=fsd['Sat_SD'], color='blue', capsize=3, linewidth=0.7)


    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    #finner_df.plot(y='Sat_inner_mean', ax=axes, color='orange')
    fid.plot(y='Field', ax=axes, color='red', linewidth=0.7)
    plt.errorbar(x=fid.index, y=fid['Field'], yerr=fid['Field_SD'], color='red', capsize=3, linewidth=0.7)

    axes.set_xlabel('Band Number')
    axes.set_ylabel('Reflectance')
    axes.set_xlim(-0.5,len(fstat_df.index)-0.5)

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_InnerFieldBandCompare.png', dpi=300)
