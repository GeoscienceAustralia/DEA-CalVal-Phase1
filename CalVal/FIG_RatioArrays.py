import matplotlib.pyplot as plt


#
## Figure 
#
### Plot ratio arrays for each band
#
# Each panel shows the ratio of satellite/field data.
#
def FIG_ratio_arrays(sat_array, field_array, output, field_data, fignum):
    newarr = sat_array/field_array
    newarr.reset_index('time', drop=True, inplace=True)

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(11.5, 9.5))
    fig.suptitle(fig_title+': Ratio of satellite/field reflectance', fontweight='bold')

    newarr.coastal_aerosol.plot(ax=axes[0,0])
    newarr.blue.plot(ax=axes[0,1])
    newarr.green.plot(ax=axes[0,2])
    newarr.red.plot(ax=axes[1,0])
    newarr.nir.plot(ax=axes[1,1])
    newarr.swir1.plot(ax=axes[1,2])
    newarr.swir2.plot(ax=axes[2,0])
    plt.tight_layout(pad=3.0, w_pad=1.0, h_pad=1.0)

    axes[2,1].axis('off')
    axes[2,2].axis('off')
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_RatioSatOverFieldData.png')
