import matplotlib.pyplot as plt


#
### Figure 
#
# Histograms of individual spectra by band
#
# The histograms can be used to identify bad ground data, through outliers.
#
def FIG_spec_histogram(ls_ground_bands, s2_ground_bands, output, field_data, fignum):

    if field_data[3] == 'Landsat8':
        fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(9.5, 9.5))
        plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.3)
        
        bands_only = ls_ground_bands.filter(like='band')
        for count, i in enumerate(bands_only):
            ls_ground_bands[i].hist(bins=50, ax=axes[int(count/3),count%3])
            axes[int(count/3),count%3].set_title(i)
        axes[2,1].axis('off')
        axes[2,2].axis('off')

    else:
        fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(9.5, 9.5))
        plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.3)
        
        bands_only = s2_ground_bands.filter(like='band')
        for count, i in enumerate(bands_only):
            s2_ground_bands[i].hist(bins=50, ax=axes[int(count/3),count%3])
            axes[int(count/3),count%3].set_title(i)
        axes[3,2].axis('off')

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_BandHistograms.png')
