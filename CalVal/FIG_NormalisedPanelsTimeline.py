import numpy as np
import matplotlib.pyplot as plt


#
## Figure 
#
### Create timeline plot of averaged, normalised all/good panels
#
#    These plots are used to identify any panels that show unusually bright or
#    dark readings, which can be weeded out as bad panels.
#    
# The general shape of the curve should follow "insolation" - the changing of
# incident light due to the Sun rising/falling in the sky.
#
# The method to create the normalised mean panels is as follows:
#
#    1. A mask of the mean good panels is created that removes the wavelengths
#       that are most affected by low atmospheric transmission.
#    2. ALL/GOOD spectra are divided by the masked mean good panel spectrum to
#       make normalised spectra.
#    3. The mean values for both ALL and GOOD normalised spectra are created.
#    4. The mean values for spectra are appended to the spt and gpta dataframes.
#    5. The mean values are plotted, as a function of time, relative to the
#       first panel time stamp.
#
def normalise_spectra(good_panel_mean, good_panel_spec, all_panel_spec, gpt, gpta):
    #
    # Create a mask to avoid wavelengths where atmospheric transmission is
    # close to zero: 1350-1480nm, 1801-1966nm and >2350nm
    #
    mask1 = good_panel_mean.where(np.logical_or(good_panel_mean.index<1350, good_panel_mean.index>1480))
    mask2 = mask1.where(np.logical_or(mask1.index<1801, mask1.index>1966))

    # 1.
    mean_panel_masked = mask2.where(np.logical_or(mask2.index<2350, mask2.index>2500))

    # 2.
    good_norm_panels_masked = good_panel_spec.div(mean_panel_masked, axis=0)
    all_norm_panels_masked = all_panel_spec.div(mean_panel_masked, axis=0)

    # 3.
    good_averages_masked = good_norm_panels_masked.mean(axis=0)
    all_averages_masked = all_norm_panels_masked.mean(axis=0)

    # 4.
    gpt['Normalised_Averaged_Panels']=good_averages_masked.values
    gpta['Normalised_Averaged_Panels']=all_averages_masked.values
    
    return gpt, gpta

#
#
#
def FIG_normalised_panels_timeline(gpt, gpta, output, field_data, fignum):
    # 5.
    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9.5, 4.5))
    fig.suptitle(fig_title+': Time vs Normalised, Wavelength-averaged Panels', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    gpta.plot.scatter(x='date_saved', y='Normalised_Averaged_Panels', title='All Panels', color='black', ax=axes[0])
    gpta.plot.line(x='date_saved', y='Normalised_Averaged_Panels', ax=axes[0], style='b', legend=False)
    axes[0].set_ylabel("Normalised Average Panel Radiance")
    axes[0].set_xlabel("Time (seconds)")

    gpt.plot.scatter(x='date_saved', y='Normalised_Averaged_Panels', title='Good Panels', color='black', ax=axes[1])
    gpt.plot.line(x='date_saved', y='Normalised_Averaged_Panels', ax=axes[1], style='b', legend=False)
    axes[1].set_ylabel("")
    axes[1].set_xlabel("Time (seconds)")

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_TimevsAvgPanels.png')
