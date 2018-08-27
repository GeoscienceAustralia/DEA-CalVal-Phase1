import pandas as pd
import matplotlib.pyplot as plt


def FIG_multi_time_line(fls8_df, fs2a_df, fs2b_df, field_data, output, fignum):
    ls8_means = [col for col in fls8_df.columns if 'ls8_mean' in col]
    ls8_times = [pd.Timestamp(x[8:]).dayofyear-pd.Timestamp(field_data[1]).dayofyear for x in ls8_means]
    
    s2a_means = [col for col in fs2a_df.columns if 'S2a_mean' in col]
    s2a_times = [pd.Timestamp(x[8:]).dayofyear-pd.Timestamp(field_data[1]).dayofyear for x in s2a_means]
    
    s2b_means = [col for col in fs2b_df.columns if 'S2b_mean' in col]
    s2b_times = [pd.Timestamp(x[8:]).dayofyear-pd.Timestamp(field_data[1]).dayofyear for x in s2b_means]
    

    #############
    # Landsat 8 #
    #############

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]
    fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(12.5, 18.5))
    fig.suptitle(fig_title+': Landsat 8 (black) and Field data (blue) comparison', fontweight='bold')
    plt.tight_layout(pad=6.5, w_pad=1.0, h_pad=1.5)
    
    axes[0,0].set_title('Coastal Aerosol')
    axes[0,1].set_title('Blue')
    axes[1,0].set_title('Green')
    axes[1,1].set_title('Red')
    axes[2,0].set_title('NIR')
    axes[2,1].set_title('SWIR 1')
    axes[3,0].set_title('SWIR 2')
    axes[3,1].axis('off')
    
    axes[0,0].scatter(x=ls8_times, y=fls8_df.loc['band1'][ls8_means], color='black')
    axes[0,0].scatter(x=0, y=fls8_df.loc['band1']['Field_mean'], color='blue')
    
    axes[0,1].scatter(x=ls8_times, y=fls8_df.loc['band2'][ls8_means], color='black')
    axes[0,1].scatter(x=0, y=fls8_df.loc['band2']['Field_mean'], color='blue')
    
    axes[1,0].scatter(x=ls8_times, y=fls8_df.loc['band3'][ls8_means], color='black')
    axes[1,0].scatter(x=0, y=fls8_df.loc['band3']['Field_mean'], color='blue')
    
    axes[1,1].scatter(x=ls8_times, y=fls8_df.loc['band4'][ls8_means], color='black')
    axes[1,1].scatter(x=0, y=fls8_df.loc['band4']['Field_mean'], color='blue')
    
    axes[2,0].scatter(x=ls8_times, y=fls8_df.loc['band5'][ls8_means], color='black')
    axes[2,0].scatter(x=0, y=fls8_df.loc['band5']['Field_mean'], color='blue')
    
    axes[2,1].scatter(x=ls8_times, y=fls8_df.loc['band6'][ls8_means], color='black')
    axes[2,1].scatter(x=0, y=fls8_df.loc['band6']['Field_mean'], color='blue')
    
    axes[3,0].scatter(x=ls8_times, y=fls8_df.loc['band7'][ls8_means], color='black')
    axes[3,0].scatter(x=0, y=fls8_df.loc['band7']['Field_mean'], color='blue')
    
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+'Landsat 8'+'_'+'Fig'+str(fignum)+'_MultiTimeLine.png')

    ############
    # Sentinel #
    ############

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(12.5, 12.5))
    fig.suptitle(fig_title+': Sentinel 2a (green), Sentinel 2b (black) and Field data (blue) comparison', fontweight='bold')
    plt.tight_layout(pad=6.5, w_pad=1.0, h_pad=1.5)
    
    axes[0,0].set_title('Coastal Aerosol')
    axes[0,1].set_title('Blue')
    axes[0,2].set_title('Green')
    axes[1,0].set_title('Red')
    axes[1,1].set_title('Red Edge 1')
    axes[1,2].set_title('Red Edge 2')
    axes[2,0].set_title('Red Edge 3')
    axes[2,1].set_title('NIR 1')
    axes[2,2].set_title('NIR 2')
    axes[3,0].set_title('SWIR 2')
    axes[3,1].set_title('SWIR 3')
    axes[3,2].axis('off')

    axes[0,0].scatter(x=s2a_times, y=fs2a_df.loc['band1'][s2a_means], color='green')
    axes[0,0].scatter(x=0, y=fs2a_df.loc['band1']['Field_mean'], color='blue')
    axes[0,0].scatter(x=s2b_times, y=fs2b_df.loc['band1'][s2b_means], color='black')
    axes[0,0].scatter(x=0, y=fs2b_df.loc['band1']['Field_mean'], color='blue')
    
    axes[0,1].scatter(x=s2a_times, y=fs2a_df.loc['band2'][s2a_means], color='green')
    axes[0,1].scatter(x=0, y=fs2a_df.loc['band2']['Field_mean'], color='blue')
    axes[0,1].scatter(x=s2b_times, y=fs2b_df.loc['band2'][s2b_means], color='black')
    axes[0,1].scatter(x=0, y=fs2b_df.loc['band2']['Field_mean'], color='blue')
    
    axes[0,2].scatter(x=s2a_times, y=fs2a_df.loc['band3'][s2a_means], color='green')
    axes[0,2].scatter(x=0, y=fs2a_df.loc['band3']['Field_mean'], color='blue')
    axes[0,2].scatter(x=s2b_times, y=fs2b_df.loc['band3'][s2b_means], color='black')
    axes[0,2].scatter(x=0, y=fs2b_df.loc['band3']['Field_mean'], color='blue')
    
    axes[1,0].scatter(x=s2a_times, y=fs2a_df.loc['band4'][s2a_means], color='green')
    axes[1,0].scatter(x=0, y=fs2a_df.loc['band4']['Field_mean'], color='blue')
    axes[1,0].scatter(x=s2b_times, y=fs2b_df.loc['band4'][s2b_means], color='black')
    axes[1,0].scatter(x=0, y=fs2b_df.loc['band4']['Field_mean'], color='blue')
    
    axes[1,1].scatter(x=s2a_times, y=fs2a_df.loc['band5'][s2a_means], color='green')
    axes[1,1].scatter(x=0, y=fs2a_df.loc['band5']['Field_mean'], color='blue')
    axes[1,1].scatter(x=s2b_times, y=fs2b_df.loc['band5'][s2b_means], color='black')
    axes[1,1].scatter(x=0, y=fs2b_df.loc['band5']['Field_mean'], color='blue')
    
    axes[1,2].scatter(x=s2a_times, y=fs2a_df.loc['band6'][s2a_means], color='green')
    axes[1,2].scatter(x=0, y=fs2a_df.loc['band6']['Field_mean'], color='blue')
    axes[1,2].scatter(x=s2b_times, y=fs2b_df.loc['band6'][s2b_means], color='black')
    axes[1,2].scatter(x=0, y=fs2b_df.loc['band6']['Field_mean'], color='blue')
    
    axes[2,0].scatter(x=s2a_times, y=fs2a_df.loc['band7'][s2a_means], color='green')
    axes[2,0].scatter(x=0, y=fs2a_df.loc['band7']['Field_mean'], color='blue')
    axes[2,0].scatter(x=s2b_times, y=fs2b_df.loc['band7'][s2b_means], color='black')
    axes[2,0].scatter(x=0, y=fs2b_df.loc['band7']['Field_mean'], color='blue')
    
    axes[2,1].scatter(x=s2a_times, y=fs2a_df.loc['band8'][s2a_means], color='green')
    axes[2,1].scatter(x=0, y=fs2a_df.loc['band8']['Field_mean'], color='blue')
    axes[2,1].scatter(x=s2b_times, y=fs2b_df.loc['band8'][s2b_means], color='black')
    axes[2,1].scatter(x=0, y=fs2b_df.loc['band8']['Field_mean'], color='blue')
    
    axes[2,2].scatter(x=s2a_times, y=fs2a_df.loc['band8a'][s2a_means], color='green')
    axes[2,2].scatter(x=0, y=fs2a_df.loc['band8a']['Field_mean'], color='blue')
    axes[2,2].scatter(x=s2b_times, y=fs2b_df.loc['band8a'][s2b_means], color='black')
    axes[2,2].scatter(x=0, y=fs2b_df.loc['band8a']['Field_mean'], color='blue')
    
    axes[3,0].scatter(x=s2a_times, y=fs2a_df.loc['band11'][s2a_means], color='green')
    axes[3,0].scatter(x=0, y=fs2a_df.loc['band11']['Field_mean'], color='blue')
    axes[3,0].scatter(x=s2b_times, y=fs2b_df.loc['band11'][s2b_means], color='black')
    axes[3,0].scatter(x=0, y=fs2b_df.loc['band11']['Field_mean'], color='blue')
    
    axes[3,1].scatter(x=s2a_times, y=fs2a_df.loc['band12'][s2a_means], color='green')
    axes[3,1].scatter(x=0, y=fs2a_df.loc['band12']['Field_mean'], color='blue')
    axes[3,1].scatter(x=s2b_times, y=fs2b_df.loc['band12'][s2b_means], color='black')
    axes[3,1].scatter(x=0, y=fs2b_df.loc['band12']['Field_mean'], color='blue')
    
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_Sentinel 2a_b_'+'Fig'+str(fignum)+'_MultiTimeLine.png')
