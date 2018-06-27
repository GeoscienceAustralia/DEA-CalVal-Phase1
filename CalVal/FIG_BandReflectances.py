import pandas as pd
import matplotlib.pyplot as plt


#
# ### Figure 
#
# Plot band reflectances
#
def FIG_band_reflectances(ground_bands, result_df, band, colpac, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(11.5, 6.5))
    fig.suptitle(fig_title+': \nGround Reflectances averaged into '+field_data[3]+' Bands\n        Line Averaged                                                         Individual spectra', fontweight='bold')
    axes[0].set_ylabel("Reflectance")
    axes[0].set_xlabel("Band Number")
    axes[1].set_xlabel("Band Number")
    axes[0].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    axes[1].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    plt.tight_layout(pad=5.5, w_pad=1.0, h_pad=1.0)

    d=pd.DataFrame([[[ground_bands[j][(ground_bands['Line']==i)].mean()] for j in list(band.keys())] for i in ground_bands.Line.unique()])
    for i in d.columns:
        d[i] = d[i].str.get(0)
        d.rename(columns={i: 'band'+str(i+1)}, inplace=True)
    for i in d.index:
        d.rename(index={i: 'Line'+str(i+1)}, inplace=True)

    d.T.plot(legend=True, ax=axes[0], color=colpac)

    result_df.T.plot(legend=False, ax=axes[1])

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_BandReflectances.png')
