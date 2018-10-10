import numpy as np
import pandas as pd

def make_adjacent_time_stats(fls8_df, fs2a_df, fs2b_df, rain_dat):

    krain = pd.read_csv(rain_dat)
    krain.set_index('day', inplace=True)

    ls8_means = [col for col in fls8_df.columns if 'ls8_mean' in col]
    ls8_times = [(pd.Timestamp(x[8:])-pd.Timestamp(2018,1,1)).days for x in ls8_means]

    s2a_means = [col for col in fs2a_df.columns if 'S2a_mean' in col]
    s2a_times = [(pd.Timestamp(x[8:])-pd.Timestamp(2018,1,1)).days for x in s2a_means]

    s2b_means = [col for col in fs2b_df.columns if 'S2b_mean' in col]
    s2b_times = [(pd.Timestamp(x[8:])-pd.Timestamp(2018,1,1)).days for x in s2b_means]

    dfl = []

    # SENTINEL 2a
    for j in fs2a_df.index:  # Loop over bands
        for i in range(1, len(s2a_times)):  # Loop over times
            if (s2a_times[i]-s2a_times[i-1]) < 17:   # If there are two times within 17 days of each other...
                tempdf = pd.DataFrame([[float(fs2a_df.loc[j][s2a_means][i-1]),
                                        float(fs2a_df.loc[j][s2a_means][i]-fs2a_df.loc[j][s2a_means][i-1])]],
                                        columns = ['SR'+str(j), 'Diff'+str(j)])
                dfl.append(tempdf)

        
        df_s2a = pd.concat(dfl, ignore_index=True, axis=0, sort=False)
    dfl = []
        
    # SENTINEL 2b
    for j in fs2b_df.index:  # Loop over bands
        for i in range(1, len(s2b_times)):  # Loop over times
            if (s2b_times[i]-s2b_times[i-1]) < 17:   # If there are two times within 17 days of each other...
                tempdf = pd.DataFrame([[float(fs2b_df.loc[j][s2b_means][i-1]),
                                        float(fs2b_df.loc[j][s2b_means][i]-fs2b_df.loc[j][s2b_means][i-1])]],
                                        columns = ['SR'+str(j), 'Diff'+str(j)])
                dfl.append(tempdf)

        
        df_s2b = pd.concat(dfl, ignore_index=True, axis=0, sort=False)
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

    return df_s2a, df_s2b, df_ls8, ls8_times, s2a_times, s2b_times


def calc_stats(fls8_df, fs2a_df, fs2b_df, rain_dat):
    df_s2a, df_s2b, df_ls8, ls8_times, s2a_times, s2b_times  = make_adjacent_time_stats(fls8_df, fs2a_df, fs2b_df, rain_dat)
    
    sband = {0: 1, 1: 2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:8, 8:'8a', 9:11, 10:12}
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
    dd1_s2a = df_s2a.filter(like='Diff').std()
    dd0_s2a = df_s2a.filter(like='SR').mean()

    print('\nSENTINEL 2a: Number of adjacent overpasses:', len(s2a_times))
    for i in range(len(dd0_s2a)):
        print('Sentinel 2a Surface Reflectance for Band',
                sband[i],
                'is',
                str(round(dd0_s2a[i], 3)) + '+/-' + str(round(dd1_s2a[i], 3)),
                '(' + str(round(100*dd1_s2a[i]/dd0_s2a[i], 2)) + '%)'
                )
    dd1_s2b = df_s2b.filter(like='Diff').std()
    dd0_s2b = df_s2b.filter(like='SR').mean()

    print('\nSENTINEL 2b: Number of adjacent overpasses:', len(s2b_times))
    for i in range(len(dd0_s2b)):
        print('Sentinel 2b Surface Reflectance for Band',
                sband[i],
                'is',
                str(round(dd0_s2b[i], 3)) + '+/-' + str(round(dd1_s2b[i], 3)),
                '(' + str(round(100*dd1_s2b[i]/dd0_s2b[i], 2)) + '%)'
                )

    return dd0_ls8, dd1_ls8, dd0_s2a, dd1_s2a, dd0_s2b, dd1_s2b
