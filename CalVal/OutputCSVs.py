import pandas as pd


def output_csvs(ls_fstat_WSdf, ls_fstat_usgs_df, s2_fstat_df, ls_sat_array, s2_sat_array, ls_ground_WSbrdf, s2_ground_brdf, field_data):

    ls_fstat_WSdf.to_csv('../CSV/'+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_Landsat8.csv')
    s2_fstat_df.to_csv('../CSV/'+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_Sentinel2.csv')
    if field_data[6] == 'USGS':
        ls_fstat_usgs_df.to_csv('../CSV/'+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_Landsat8_USGS.csv')

    if field_data[3] == 'Landsat8':
        if isinstance(ls_ground_WSbrdf['date_saved'].min(), pd.datetime):
            print('Difference in time between field site measurement and LS8 data is '\
                  +str(pd.to_datetime(str(ls_sat_array.time.values[0])) - ls_ground_WSbrdf['date_saved'].min()))
        else:
            print('Difference in time between field site measurement and LS8 data is '\
                  +str(pd.to_datetime(str(ls_sat_array.time.values[0])) - pd.to_datetime(ls_ground_WSbrdf['date_saved'].min())))

    else:
        if isinstance(s2_ground_brdf['date_saved'].min(), pd.datetime):
            print('Difference in time between field site measurement and Sentinel data is '
                  +str(pd.to_datetime(str(s2_sat_array.time.values[0])) - s2_ground_brdf['date_saved'].min()))
        else:
            print('Difference in time between field site measurement and Sentinel data is '
                  +str(pd.to_datetime(str(s2_sat_array.time.values[0])) - pd.to_datetime(s2_ground_brdf['date_saved'].min())))
