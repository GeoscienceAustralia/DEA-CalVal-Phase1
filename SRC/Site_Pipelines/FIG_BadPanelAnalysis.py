import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#
## Figure
#
### Diagnosis plots of bad panel spectra
#
# Create a mean of the good panel readings, as well as the bad panel
# readings. Then a ratio and a difference of the two can be (seperately)
# created and plotted.
#
# Since the two bad panel readings are higher than they should be, we
# put the bad panels on the top of the division and first in the
# difference.
#
def FIG_bad_panel_analysis(good_panel_mean, good_panel_spec, bad_panel_spec, output, field_data, fignum):

    bad_panel_mean = bad_panel_spec.mean(axis=1)

    good_bad_div = bad_panel_mean.div(good_panel_mean, axis=0)
    good_bad_diff = bad_panel_mean.sub(good_panel_mean, axis=0)

    pd.Series.to_frame(good_bad_div)
    pd.Series.to_frame(good_bad_diff)

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(9.5, 9.5))
    #fig.suptitle(fig_title, fontweight='bold')

    good_bad_div.plot(title='(average bad panels / average good panels)', legend=False, ax=axes[0,0])
    axes[0,0].set_xlabel('Wavelength (nm)')

    good_bad_diff.plot(title='(average bad panels) - (average good panels)', legend=False, ax=axes[0,1])
    axes[0,1].set_xlabel('Wavelength (nm)')

    good_panel_mean.plot(title='Average good panels', legend=False, ax=axes[1,0])
    axes[1,0].set_ylabel("Radiance (W m$^{-2}$ nm$^{-1}$ sr$^{-1}$)")
    axes[1,0].set_xlabel('Wavelength (nm)')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    bad_panel_mean.plot(title='Average bad panels', legend=False, ax=axes[1,1])
    axes[1,1].set_ylabel("Radiance (W m$^{-2}$ nm$^{-1}$ sr$^{-1}$)")
    axes[1,1].set_xlabel('Wavelength (nm)')
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_GoodBadPanelCompare.png')

