import numpy as np
import pandas as pd

def make_adjacent_time_stats(fls8_df, fls8_usgs_df):

    ls8_means = [col for col in fls8_df.columns if 'ls8_mean' in col]
    ls8_times = [(pd.Timestamp(x[8:])-pd.Timestamp(2018,1,1)).days for x in ls8_means]

    ls8_usgs_means = [col for col in fls8_usgs_df.columns if 'ls8_mean' in col]
    ls8_usgs_times = [(pd.Timestamp(x[8:])-pd.Timestamp(2018,1,1)).days for x in ls8_usgs_means]

    dfl = []

    # LANDSAT 8
    for j in fls8_df.index:  # Loop over bands
        for i in range(1, len(ls8_times)):  # Loop over times
            if (ls8_times[i]-ls8_times[i-1]) < 17:   # If there are two times within 17 days of each other...
                tempdf = pd.DataFrame([[float(fls8_df.loc[j][ls8_means][i-1]),
                                        float(fls8_df.loc[j][ls8_means][i]-fls8_df.loc[j][ls8_means][i-1])]],
                                        columns = ['SR'+str(j), 'Diff'+str(j)])
                dfl.append(tempdf)
        
        df_ls8 = pd.concat(dfl, ignore_index=True, axis=0, sort=False)

    dfl = []

    # LANDSAT 8 USGS
    for j in fls8_usgs_df.index:  # Loop over bands
        for i in range(1, len(ls8_usgs_times)):  # Loop over times
            if (ls8_usgs_times[i]-ls8_usgs_times[i-1]) < 17:   # If there are two times within 17 days of each other...
                tempdf = pd.DataFrame([[float(fls8_usgs_df.loc[j][ls8_usgs_means][i-1]),
                                        float(fls8_usgs_df.loc[j][ls8_usgs_means][i]-fls8_usgs_df.loc[j][ls8_usgs_means][i-1])]],
                                        columns = ['SR'+str(j), 'Diff'+str(j)])
                dfl.append(tempdf)
        
        df_usgs_ls8 = pd.concat(dfl, ignore_index=True, axis=0, sort=False)

    return df_ls8, df_usgs_ls8, ls8_times, ls8_usgs_times


def calc_stats(fls8_df, fls8_usgs_df):
    df_ls8, df_usgs_ls8, ls8_times, ls8_usgs_times = make_adjacent_time_stats(fls8_df, fls8_usgs_df)
    
    lband = {0: 1, 1: 2, 2:3, 3:4, 4:5, 5:6, 6:7}

    dd1_ls8 = df_ls8.filter(like='Diff').std()
    dd0_ls8 = df_ls8.filter(like='SR').mean()

    print('LANDSAT 8: Number of adjacent overpasses:', len(ls8_times))
    for i in range(len(dd0_ls8)):
        print('Landsat 8 Surface Reflectance for Band',
                lband[i],
                'is',
                str(round(dd0_ls8[i], 3)) + '+/-' + str(round(dd1_ls8[i], 3)),
                '(' + str(round(100*dd1_ls8[i]/dd0_ls8[i], 2)) + '%)'
                )

    dd1_usgs_ls8 = df_usgs_ls8.filter(like='Diff').std()
    dd0_usgs_ls8 = df_usgs_ls8.filter(like='SR').mean()

    print('LANDSAT 8 USGS: Number of adjacent overpasses:', len(ls8_usgs_times))
    for i in range(len(dd0_usgs_ls8)):
        print('Landsat 8 USGS Surface Reflectance for Band',
                lband[i],
                'is',
                str(round(dd0_usgs_ls8[i], 3)) + '+/-' + str(round(dd1_usgs_ls8[i], 3)),
                '(' + str(round(100*dd1_usgs_ls8[i]/dd0_usgs_ls8[i], 2)) + '%)'
                )

    return dd0_ls8, dd1_ls8, dd0_usgs_ls8, dd1_usgs_ls8
