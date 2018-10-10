import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#
# ### Figure 
#
# Plot band reflectances
#
def FIG_reflectances_band(ground_bands, result_df, band, good_panels, all_refls, colpac, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(7.5, 3.0))
    plt.tight_layout(pad=2.5, w_pad=-2.0, h_pad=1.0)
#    fig.suptitle(fig_title+': \nGround Reflectances averaged into '+field_data[3]+' Bands\n        Line Averaged                                                         Individual spectra', fontweight='bold')
    axes[1].set_xlabel("Band Number")
    axes[1].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])


    maska = all_refls[np.logical_xor(all_refls.index > 1350, all_refls.index < 1480)]
    maskb = maska[np.logical_xor(maska.index > 1801, maska.index < 1966)]
    all_refls_masked = maskb[(maskb.index < 2350)]

    axes[0].set_ylabel("Reflectance")
    axes[0].set_ylim(all_refls_masked.min().min()*0.95, all_refls_masked.max().max()*1.05)
    axes[1].set_ylim(all_refls_masked.min().min()*0.95, all_refls_masked.max().max()*1.05)

    all_refls.plot(legend=False, ax=axes[0], color='#AAAAAA', linewidth=0.7)

    for i in good_panels.Line.unique():
        rad_name = 'radiance'+str(i)
        line = all_refls.filter(like=rad_name).mean(axis=1)
        line.plot(ax=axes[0], color=colpac[i], legend=False, label='Line'+str(i), linewidth=0.7)

    d=pd.DataFrame([[[ground_bands[j][(ground_bands['Line']==i)].mean()] for j in list(band.keys())] for i in ground_bands.Line.unique()])
    for i in d.columns:
        d[i] = d[i].str.get(0)
        d.rename(columns={i: str(i+1)}, inplace=True)
    for i in d.index:
        d.rename(index={i: 'Line'+str(i+1)}, inplace=True)
    d.rename({'9': '8a', '10':'11', '11':'12'}, axis=1, inplace=True)

    d.T.plot(legend=False, ax=axes[1], color=colpac, sharey=True, linewidth=0.7)

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_Reflectances_Band.png', dpi=300)
