import numpy as np
from datetime import timedelta


#
### Create dataframe with relative time stamps
#
# Make a new dataframe with time since the first good panel reading
# along the x-axis and "1" for the y-axis. This allows a plot of the
# data timeline to be made.
#
def make_timeline(in_df, good_panels):
    
    temp_df = in_df[['date_saved', 'Line']].loc[in_df['Wavelength']==350]
    gpt = good_panels[['date_saved', 'Line']].loc[good_panels['Wavelength']==350]
    
    out_df = temp_df.copy()

    for i in range(len(out_df)):
        out_df.iloc[[i], [0]]=int((temp_df.iloc[i][0]-gpt.iloc[0][0]).total_seconds())

    out_df['ones'] = np.ones(len(out_df))
    return out_df

#
### Create time-relative dataframes
#
#   gpt = good panels
#   gpta = all panels
#   adt = good grounds
#   adta = all grounds
#
def create_time_relative_dfs(good_panels, all_panels, good_grounds, all_grounds):
    
    gpt = make_timeline(good_panels, good_panels)
    gpta = make_timeline(all_panels, good_panels)
    adt = make_timeline(good_grounds, good_panels)
    adta = make_timeline(all_grounds, good_panels)
    
    return gpt, gpta, adt, adta
