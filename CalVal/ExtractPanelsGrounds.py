from datetime import datetime
#
###Specify which spectra are panels/ground/good/bad
#
# Determine panel file names by assuming that all panels have a data value of
# at least 0.06 in the first wavelength (350nm). Call this dataframe 'panel_names'.
#
#   good_panels = all panel data with bad panels removed
#   bad_panels = all bad panel data
#   all_panels = both good and bad panel data
#   good_grounds = good ground readings
#   all_grounds = all ground data.
#
# Any bad ground data (bad_grounds) is defined in the 2nd cell.
#
def extract_panels_grounds(alldata, bad_pans, bad_grounds):
    panel_names = alldata[(alldata['Wavelength']==350) & (alldata['radiance']>=0.06)]['filename']

    all_panels = alldata.loc[alldata['filename'].isin(panel_names)]
    good_panels = all_panels.loc[~all_panels['filename'].isin(bad_pans)]
    bad_panels = alldata.loc[alldata['filename'].isin(bad_pans)]

    tmp_grounds = alldata.loc[~alldata['filename'].isin(bad_grounds)]
    good_grounds = tmp_grounds.loc[~tmp_grounds['filename'].isin(panel_names)]
    all_grounds = alldata.loc[~alldata['filename'].isin(panel_names)]
    
    return panel_names, all_panels, good_panels, bad_panels, good_grounds, all_grounds
