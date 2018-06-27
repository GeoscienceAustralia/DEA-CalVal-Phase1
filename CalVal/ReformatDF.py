import pandas as pd


#
### Reformat band reflectances and apply to dataframe "ground_bands"
#
def reformat_df(good_grounds, result_df):
    gg = good_grounds[(good_grounds['Wavelength']==350)]
    gg.reset_index(drop=True, inplace=True)

    catty = pd.concat([gg,result_df], axis=1)
    ground_bands = catty.drop(['Wavelength', 'radiance'], axis=1)
    return ground_bands
