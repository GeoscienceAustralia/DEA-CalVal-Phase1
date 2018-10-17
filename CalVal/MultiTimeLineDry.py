import pandas as pd

def multi_time_line_dry(fls8_df, fs2a_df, fs2b_df, ls8_csvs, sent_csvs, rain_dat, field_data, output, fignum):

    krain = pd.read_csv(rain_dat)
    krain.rename({'Rainfall amount (millimetres)': 'rain'}, axis=1, inplace=True)
    krain['rainday'] = [(pd.Timestamp(krain.Year[i], krain.Month[i], krain.Day[i])-pd.Timestamp(2018,1,1)).days for i in range(len(krain.Year))]
    krain.set_index('rainday', inplace=True)
    
    ls8_means = [col for col in fls8_df.columns if 'ls8_mean' in col]
    ls8_times = [(pd.Timestamp(x[8:])-pd.Timestamp(2018,1,1)).days for x in ls8_means]
    
    s2a_means = [col for col in fs2a_df.columns if 'S2a_mean' in col]
    s2a_times = [(pd.Timestamp(x[8:])-pd.Timestamp(2018,1,1)).days for x in s2a_means]
    
    s2b_means = [col for col in fs2b_df.columns if 'S2b_mean' in col]
    s2b_times = [(pd.Timestamp(x[8:])-pd.Timestamp(2018,1,1)).days for x in s2b_means]
    
    for i in range(len(ls8_times)):
        rainsum = float(krain.rain[(krain.index >= ls8_times[i]-10) & (krain.index <= ls8_times[i]+1)].sum())
        if rainsum > 0:
            fls8_df.drop(ls8_means[i], axis=1, inplace=True)
            
    for i in range(len(s2a_times)):
        rainsum = float(krain.rain[(krain.index >= s2a_times[i]-10) & (krain.index <= s2a_times[i]+1)].sum())
        if rainsum > 0:
            fs2a_df.drop(s2a_means[i], axis=1, inplace=True)
            
    for i in range(len(s2b_times)):
        rainsum = float(krain.rain[(krain.index >= s2b_times[i]-10) & (krain.index <= s2b_times[i]+1)].sum())
        if rainsum > 0:
            fs2b_df.drop(s2b_means[i], axis=1, inplace=True)
