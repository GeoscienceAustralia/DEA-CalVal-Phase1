import matplotlib.pyplot as plt


#
### Figure 
#
# Histograms of individual spectra by band
#
# The histograms can be used to identify bad ground data, through outliers.
#
def FIG_spec_histogram(ground_bands, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=0.3)
    
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9.5, 9.5))
    bands_only = ground_bands.filter(like='band')
    bands_only.hist(bins=50, ax=axes)
    fig.suptitle(fig_title+': Histograms by band for individual spectra', fontweight='bold')

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_BandHistograms.png')
