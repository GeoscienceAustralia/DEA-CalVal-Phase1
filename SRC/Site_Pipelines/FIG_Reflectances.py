import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#
## Figure 
#
### Plot all ground reflectances in black, plus the Line-averaged reflectances
### in colour
#
# The Line-averaged reflectances are shown in order to identify any outlying
# lines that might have been caused by bad panel spectra (for example).
#
def FIG_reflectances(good_panels, all_refls, colpac, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axy = plt.subplots(nrows=1, ncols=2, figsize=(13.5, 5.5))
    fig.suptitle(fig_title+': Ground Reflectances.\nBlack: Individual reflectances. Colour: Average Reflectances for each line', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    maska = all_refls[np.logical_xor(all_refls.index > 1350, all_refls.index < 1480)]
    maskb = maska[np.logical_xor(maska.index > 1801, maska.index < 1966)]
    all_refls_masked = maskb[(maskb.index < 2350)]

    axy[0].set_ylabel("Reflectance")
    axy[1].set_ylim(all_refls_masked.min().min()*0.95, all_refls_masked.max().max()*1.05)

    all_refls.plot(legend=False, ax=axy[0], color='k')
    all_refls.plot(legend=False, ax=axy[1], color='k')

    for i in good_panels.Line.unique():
        rad_name = 'radiance'+str(i)
        line = all_refls.filter(like=rad_name).mean(axis=1)
        line.plot(ax=axy[0], color=colpac[i], legend=True, label='Line'+str(i))
        line.plot(ax=axy[1], color=colpac[i], legend=False, label='Line'+str(i))
    #
    #  Commented lines are used to produce a dataframe with line-averaged reflectances for Fuqin.
    #
    #    if i == good_panels.Line.min():
    #        alllines = line.to_frame()
    #    else:
    #        alllines = pd.concat([alllines, line.to_frame()], axis=1)
    #alllines.columns = good_panels.Line.unique()

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_Reflectances.png')
    
    #return alllines
