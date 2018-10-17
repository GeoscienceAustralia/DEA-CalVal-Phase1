import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def ReadInCSVs(ls8_csvs, sent_csvs):

    ls8_ftimes = ls8_csvs.copy()
    sent_ftimes = sent_csvs.copy()

    ls8_fdata = pd.DataFrame()
    sent_fdata = pd.DataFrame()

    for i in range(len(ls8_csvs)):
        ls8_ftimes[i] = pd.Timestamp(ls8_csvs[i][4:11]).dayofyear
        sent_ftimes[i] = pd.Timestamp(sent_csvs[i][4:11]).dayofyear
        lstemp = pd.read_csv('../CSV/'+ls8_csvs[i])
        senttemp = pd.read_csv('../CSV/'+sent_csvs[i])
        lstemp.set_index('Unnamed: 0', inplace=True)
        senttemp.set_index('Unnamed: 0', inplace=True)
        ls8_fdata[str(ls8_csvs[i][4:13])] = lstemp['Field_mean']
        sent_fdata[str(sent_csvs[i][4:13])] = senttemp['Field_mean']

    return ls8_ftimes, sent_ftimes, ls8_fdata, sent_fdata


def FIG_multi_time_line(fls8_df, fs2a_df, fs2b_df, ls8_csvs, sent_csvs, rain_dat, field_data, output, fignum):

    ls8_ftimes, sent_ftimes, ls8_fdata, sent_fdata = ReadInCSVs(ls8_csvs, sent_csvs)

    ls8_means = [col for col in fls8_df.columns if 'ls8_mean' in col]
    ls8_times = [(pd.Timestamp(x[8:])-pd.Timestamp(2018,1,1)).days for x in ls8_means]
    
    s2a_means = [col for col in fs2a_df.columns if 'S2a_mean' in col]
    s2a_times = [(pd.Timestamp(x[8:])-pd.Timestamp(2018,1,1)).days for x in s2a_means]
    
    s2b_means = [col for col in fs2b_df.columns if 'S2b_mean' in col]
    s2b_times = [(pd.Timestamp(x[8:])-pd.Timestamp(2018,1,1)).days for x in s2b_means]

    krain = pd.read_csv(rain_dat)
    krain.rename({'Rainfall amount (millimetres)': 'rain'}, axis=1, inplace=True)
    rainday = [(pd.Timestamp(krain.Year[i], krain.Month[i], krain.Day[i])-pd.Timestamp(2018,1,1)).days for i in range(len(krain.Year))]

    #############
    # Landsat 8 #
    #############

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]
    fig, axes = plt.subplots(nrows=7, ncols=1, figsize=(12.5, 18.5))
    fig.suptitle(fig_title+': Landsat 8 (black) and Field data (blue) comparison', fontweight='bold')
    plt.tight_layout(pad=6.5, w_pad=2.0, h_pad=1.5)
    fig.text(0.5, 0.04, 'Days since 01JAN18', ha='center', va='center', fontweight='bold')    
    fig.text(0.05, 0.5, 'Rainfall (mm)', ha='center', va='center', rotation='vertical', fontweight='bold')    
    fig.text(0.97, 0.5, 'Surface Reflectance', ha='center', va='center', rotation='vertical', fontweight='bold')    

    axes[0].set_title('Coastal Aerosol')
    axes[1].set_title('Blue')
    axes[2].set_title('Green')
    axes[3].set_title('Red')
    axes[4].set_title('NIR')
    axes[5].set_title('SWIR 1')
    axes[6].set_title('SWIR 2')

    tick_spacing = 10
    for i in range(7):
        axes[i].xaxis.set_minor_locator(ticker.MultipleLocator(tick_spacing))
        axes[i].grid(which='minor', color='#BBBBFF', linestyle='-', linewidth=1, axis='x', zorder=1)
        axes[i].set_xlim(-1826, ls8_times[-1])

    
    axes2 = axes[0].twinx()
    axes2.scatter(x=ls8_times, y=fls8_df.loc['band1'][ls8_means], color='black', s=20, zorder=10)
    axes2.scatter(x=ls8_ftimes, y=ls8_fdata.loc['Band1'], color='blue', s=20, zorder=10)
    axes[0].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[1].twinx()
    axes2.scatter(x=ls8_times, y=fls8_df.loc['band2'][ls8_means], color='black', s=20, zorder=10)
    axes2.scatter(x=ls8_ftimes, y=ls8_fdata.loc['Band2'], color='blue', s=20, zorder=10)
    axes[1].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[2].twinx()
    axes2.scatter(x=ls8_times, y=fls8_df.loc['band3'][ls8_means], color='black', s=20, zorder=10)
    axes2.scatter(x=ls8_ftimes, y=ls8_fdata.loc['Band3'], color='blue', s=20, zorder=10)
    axes[2].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[3].twinx()
    axes2.scatter(x=ls8_times, y=fls8_df.loc['band4'][ls8_means], color='black', s=20, zorder=10)
    axes2.scatter(x=ls8_ftimes, y=ls8_fdata.loc['Band4'], color='blue', s=20, zorder=10)
    axes[3].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[4].twinx()
    axes2.scatter(x=ls8_times, y=fls8_df.loc['band5'][ls8_means], color='black', s=20, zorder=10)
    axes2.scatter(x=ls8_ftimes, y=ls8_fdata.loc['Band5'], color='blue', s=20, zorder=10)
    axes[4].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[5].twinx()
    axes2.scatter(x=ls8_times, y=fls8_df.loc['band6'][ls8_means], color='black', s=20, zorder=10)
    axes2.scatter(x=ls8_ftimes, y=ls8_fdata.loc['Band6'], color='blue', s=20, zorder=10)
    axes[5].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[6].twinx()
    axes2.scatter(x=ls8_times, y=fls8_df.loc['band7'][ls8_means], color='black', s=20, zorder=10)
    axes2.scatter(x=ls8_ftimes, y=ls8_fdata.loc['Band7'], color='blue', s=20, zorder=10)
    axes[6].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+'Landsat 8'+'_'+'Fig'+str(fignum)+'_MultiTimeLine.png')

    ############
    # Sentinel #
    ############

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]
    fig, axes = plt.subplots(nrows=11, ncols=1, figsize=(12.5, 22.5))
    fig.suptitle(fig_title+': Sentinel 2a (green), Sentinel 2b (black) and Field data (blue) comparison', fontweight='bold')
    fig.text(0.5, 0.03, 'Days since 01JAN18', ha='center', va='center', fontweight='bold')    
    fig.text(0.05, 0.5, 'Rainfall (mm)', ha='center', va='center', rotation='vertical', fontweight='bold')    
    fig.text(0.97, 0.5, 'Surface Reflectance', ha='center', va='center', rotation='vertical', fontweight='bold')    
    plt.tight_layout(pad=6.5, w_pad=3.0, h_pad=1.5)
    
    axes[0].set_title('Coastal Aerosol')
    axes[1].set_title('Blue')
    axes[2].set_title('Green')
    axes[3].set_title('Red')
    axes[4].set_title('Red Edge 1')
    axes[5].set_title('Red Edge 2')
    axes[6].set_title('Red Edge 3')
    axes[7].set_title('NIR 1')
    axes[8].set_title('NIR 2')
    axes[9].set_title('SWIR 2')
    axes[10].set_title('SWIR 3')

    tick_spacing = 10
    for i in range(11):
        axes[i].xaxis.set_minor_locator(ticker.MultipleLocator(tick_spacing))
        axes[i].grid(which='minor', color='#BBBBFF', linestyle='-', linewidth=1, axis='x', zorder=0)
        axes[i].set_xlim(-1826, s2a_times[-1])

    axes2 = axes[0].twinx()
    axes2.scatter(x=s2a_times, y=fs2a_df.loc['band1'][s2a_means], color='green', s=20, zorder=10)
    axes2.scatter(x=s2b_times, y=fs2b_df.loc['band1'][s2b_means], color='black', s=20, zorder=10)
    axes2.scatter(x=sent_ftimes, y=sent_fdata.loc['Band1'], color='blue', s=20, zorder=10)
    axes[0].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[1].twinx()
    axes2.scatter(x=s2a_times, y=fs2a_df.loc['band2'][s2a_means], color='green', s=20, zorder=10)
    axes2.scatter(x=s2b_times, y=fs2b_df.loc['band2'][s2b_means], color='black', s=20, zorder=10)
    axes2.scatter(x=sent_ftimes, y=sent_fdata.loc['Band2'], color='blue', s=20, zorder=10)
    axes[1].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[2].twinx()
    axes2.scatter(x=s2a_times, y=fs2a_df.loc['band3'][s2a_means], color='green', s=20, zorder=10)
    axes2.scatter(x=s2b_times, y=fs2b_df.loc['band3'][s2b_means], color='black', s=20, zorder=10)
    axes2.scatter(x=sent_ftimes, y=sent_fdata.loc['Band3'], color='blue', s=20, zorder=10)
    axes[2].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[3].twinx()
    axes2.scatter(x=s2a_times, y=fs2a_df.loc['band4'][s2a_means], color='green', s=20, zorder=10)
    axes2.scatter(x=s2b_times, y=fs2b_df.loc['band4'][s2b_means], color='black', s=20, zorder=10)
    axes2.scatter(x=sent_ftimes, y=sent_fdata.loc['Band4'], color='blue', s=20, zorder=10)
    axes[3].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[4].twinx()
    axes2.scatter(x=s2a_times, y=fs2a_df.loc['band5'][s2a_means], color='green', s=20, zorder=10)
    axes2.scatter(x=s2b_times, y=fs2b_df.loc['band5'][s2b_means], color='black', s=20, zorder=10)
    axes2.scatter(x=sent_ftimes, y=sent_fdata.loc['Band5'], color='blue', s=20, zorder=10)
    axes[4].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[5].twinx()
    axes2.scatter(x=s2a_times, y=fs2a_df.loc['band6'][s2a_means], color='green', s=20, zorder=10)
    axes2.scatter(x=s2b_times, y=fs2b_df.loc['band6'][s2b_means], color='black', s=20, zorder=10)
    axes2.scatter(x=sent_ftimes, y=sent_fdata.loc['Band6'], color='blue', s=20, zorder=10)
    axes[5].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[6].twinx()
    axes2.scatter(x=s2a_times, y=fs2a_df.loc['band7'][s2a_means], color='green', s=20, zorder=10)
    axes2.scatter(x=s2b_times, y=fs2b_df.loc['band7'][s2b_means], color='black', s=20, zorder=10)
    axes2.scatter(x=sent_ftimes, y=sent_fdata.loc['Band7'], color='blue', s=20, zorder=10)
    axes[6].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[7].twinx()
    axes2.scatter(x=s2a_times, y=fs2a_df.loc['band8'][s2a_means], color='green', s=20, zorder=10)
    axes2.scatter(x=s2b_times, y=fs2b_df.loc['band8'][s2b_means], color='black', s=20, zorder=10)
    axes2.scatter(x=sent_ftimes, y=sent_fdata.loc['Band8'], color='blue', s=20, zorder=10)
    axes[7].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[8].twinx()
    axes2.scatter(x=s2a_times, y=fs2a_df.loc['band8a'][s2a_means], color='green', s=20, zorder=10)
    axes2.scatter(x=s2b_times, y=fs2b_df.loc['band8a'][s2b_means], color='black', s=20, zorder=10)
    axes2.scatter(x=sent_ftimes, y=sent_fdata.loc['Band8a'], color='blue', s=20, zorder=10)
    axes[8].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[9].twinx()
    axes2.scatter(x=s2a_times, y=fs2a_df.loc['band11'][s2a_means], color='green', s=20, zorder=10)
    axes2.scatter(x=s2b_times, y=fs2b_df.loc['band11'][s2b_means], color='black', s=20, zorder=10)
    axes2.scatter(x=sent_ftimes, y=sent_fdata.loc['Band11'], color='blue', s=20, zorder=10)
    axes[9].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    axes2 = axes[10].twinx()
    axes2.scatter(x=s2a_times, y=fs2a_df.loc['band12'][s2a_means], color='green', s=20, zorder=10)
    axes2.scatter(x=s2b_times, y=fs2b_df.loc['band12'][s2b_means], color='black', s=20, zorder=10)
    axes2.scatter(x=sent_ftimes, y=sent_fdata.loc['Band12'], color='blue', s=20, zorder=10)
    axes[10].plot(rainday, krain.rain, c='#FFBBBB', zorder = 5)
    
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_Sentinel 2a_b_'+'Fig'+str(fignum)+'_MultiTimeLine.png')
