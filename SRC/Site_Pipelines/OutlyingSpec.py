import pandas


def outlying_spec(ls_ground_bands, s2_ground_bands, field_data):

    if field_data[3] == 'Landsat8':
        maxfile = ls_ground_bands['filename'][(ls_ground_bands['band1'] == ls_ground_bands['band1'].max())]
        maxbands = ls_ground_bands.filter(like='band')[(ls_ground_bands['band1'] == ls_ground_bands['band1'].max())]
        minfile = ls_ground_bands['filename'][(ls_ground_bands['band1'] == ls_ground_bands['band1'].min())]
        minbands = ls_ground_bands.filter(like='band')[(ls_ground_bands['band1'] == ls_ground_bands['band1'].min())]
    else:
        maxfile = s2_ground_bands['filename'][(s2_ground_bands['band1'] == s2_ground_bands['band1'].max())]
        maxbands = s2_ground_bands.filter(like='band')[(s2_ground_bands['band1'] == s2_ground_bands['band1'].max())]
        minfile = s2_ground_bands['filename'][(s2_ground_bands['band1'] == s2_ground_bands['band1'].min())]
        minbands = s2_ground_bands.filter(like='band')[(s2_ground_bands['band1'] == s2_ground_bands['band1'].min())]
    
    print("Maximum value found in:", maxfile.iloc[0], '\n', maxbands.iloc[0], '\nMinimum value found in:', minfile.iloc[0], '\n', minbands.iloc[0])
