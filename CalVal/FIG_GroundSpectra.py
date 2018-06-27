import matplotlib.pyplot as plt


#
## Figure 
#
### Plot ground spectra (all and good), normalised to the median good spectrum
#
# These plots are used to identify any ground spectra that are bogus.
#
def FIG_ground_spectra(good_grounds_spec, all_grounds_spec, output, field_data, fignum):
    good_median = good_grounds_spec.median(axis=1)
    good_norm = good_grounds_spec.div(good_median, axis=0)
    all_norm = all_grounds_spec.div(good_median, axis=0)

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9.6, 6.0))
    fig.suptitle(fig_title, fontweight='bold')
    plt.tight_layout(pad=5.5, w_pad=1.0, h_pad=1.0)

    all_norm.plot(title="All ground radiances normalised to \nthe median ground radiance", legend=False, ax=axes[0])

    good_norm.plot(title="Good ground radiances normalised to \nthe median ground radiance", legend=False, ax=axes[1])

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_GroundRadiances.png')
