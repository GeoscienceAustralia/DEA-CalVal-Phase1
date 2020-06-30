import pandas as pd
import matplotlib.pyplot as plt

def FIG_USGS_compare_difference(fls8_df, fls8_usgs_df, output, field_data, fignum):
    diff1, diff2, diff3, diff4, diff5, diff6, diff7 = [], [], [], [], [], [], []
    band1, band2, band3, band4, band5, band6, band7 = [], [], [], [], [], [], []
    colnames = []
    coltimes = []
    
    ls8_means = [col for col in fls8_df.columns if 'ls8_mean' in col]
    
    for i in ls8_means:
        try:
            diff1.append(fls8_df.iloc[0][i]-fls8_usgs_df.iloc[0][i])
            diff2.append(fls8_df.iloc[1][i]-fls8_usgs_df.iloc[1][i])
            diff3.append(fls8_df.iloc[2][i]-fls8_usgs_df.iloc[2][i])
            diff4.append(fls8_df.iloc[3][i]-fls8_usgs_df.iloc[3][i])
            diff5.append(fls8_df.iloc[4][i]-fls8_usgs_df.iloc[4][i])
            diff6.append(fls8_df.iloc[5][i]-fls8_usgs_df.iloc[5][i])
            diff7.append(fls8_df.iloc[6][i]-fls8_usgs_df.iloc[6][i])

            band1.append(fls8_df.iloc[0][i])
            band2.append(fls8_df.iloc[1][i])
            band3.append(fls8_df.iloc[2][i])
            band4.append(fls8_df.iloc[3][i])
            band5.append(fls8_df.iloc[4][i])
            band6.append(fls8_df.iloc[5][i])
            band7.append(fls8_df.iloc[6][i])

            colnames.append(i)

        except KeyError:
            continue
    
    for i in colnames:
        coltimes.append(pd.Timestamp(i[8:]))
            
    duff = pd.DataFrame([diff1, diff2, diff3, diff4, diff5, diff6, diff7], columns=coltimes, index=['band1', 'band2', 'band3', 'band4', 'band5', 'band6', 'band7'])
    floo = pd.DataFrame([band1, band2, band3, band4, band5, band6, band7], columns=coltimes, index=['band1', 'band2', 'band3', 'band4', 'band5', 'band6', 'band7'])
    
    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]
    fig, axes = plt.subplots(nrows=7, ncols=1, figsize=(12.5, 18.5))
    fig.suptitle(fig_title+': Landsat 8 intercomparison: difference DEA-USGS', fontweight='bold')
    plt.tight_layout(pad=6.5, w_pad=2.0, h_pad=1.5)
    
    axes[0].set_title('Coastal Aerosol')
    axes[1].set_title('Blue')
    axes[2].set_title('Green')
    axes[3].set_title('Red')
    axes[4].set_title('NIR')
    axes[5].set_title('SWIR 1')
    axes[6].set_title('SWIR 2')
    
    axes[0].plot(duff.iloc[0], '-o')
    axes[1].plot(duff.iloc[1], '-o')
    axes[2].plot(duff.iloc[2], '-o')
    axes[3].plot(duff.iloc[3], '-o')
    axes[4].plot(duff.iloc[4], '-o')
    axes[5].plot(duff.iloc[5], '-o')
    axes[6].plot(duff.iloc[6], '-o')
    
    axes[0].axhline()
    axes[1].axhline()
    axes[2].axhline()
    axes[3].axhline()
    axes[4].axhline()
    axes[5].axhline()
    axes[6].axhline()
    
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'Fig'+str(fignum)+'_USGS_Compare_Difference.png')
