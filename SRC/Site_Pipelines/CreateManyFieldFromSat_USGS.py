import numpy as np


#
# ### Create Field full band xarray
#
# The field xarray is based on the pixel locations of the satellite data, where
# each pixel contains an average of all field data measurements that fall
# within the pixel.
#
def create_many_field_from_sat(ls8_array, ground_brdf_ls8, xloc):

    ###########
    # Landsat #
    ###########

    halfpix = 12.5
    field_array_ls8 = ls8_array.astype(float)

    for i in range(len(ls8_array.x)):
        for j in range(len(ls8_array.y)):
            count = 0
            cum1, cum2, cum3, cum4, cum5, cum6, cum7 = 0,0,0,0,0,0,0
            for k in range(len(xloc)):
                if (ls8_array.x[i]-halfpix < xloc[k][0] < ls8_array.x[i]+halfpix) and (ls8_array.y[j]-halfpix < xloc[k][1] < ls8_array.y[j]+halfpix):
                    cum1 = cum1+ground_brdf_ls8.iloc[k]['band1']
                    cum2 = cum2+ground_brdf_ls8.iloc[k]['band2']
                    cum3 = cum3+ground_brdf_ls8.iloc[k]['band3']
                    cum4 = cum4+ground_brdf_ls8.iloc[k]['band4']
                    cum5 = cum5+ground_brdf_ls8.iloc[k]['band5']
                    cum6 = cum6+ground_brdf_ls8.iloc[k]['band6']
                    cum7 = cum7+ground_brdf_ls8.iloc[k]['band7']
                    count=count+1
            if count < 1:
                field_array_ls8.coastal_aerosol[0][j][i] = np.nan
                field_array_ls8.blue[0][j][i] = np.nan
                field_array_ls8.green[0][j][i] = np.nan
                field_array_ls8.red[0][j][i] = np.nan
                field_array_ls8.nir[0][j][i] = np.nan
                field_array_ls8.swir1[0][j][i] = np.nan
                field_array_ls8.swir2[0][j][i] = np.nan
            else:
                field_array_ls8.coastal_aerosol[0][j][i] = cum1*10000/count            
                field_array_ls8.blue[0][j][i] = cum2*10000/count
                field_array_ls8.green[0][j][i] = cum3*10000/count
                field_array_ls8.red[0][j][i] = cum4*10000/count
                field_array_ls8.nir[0][j][i] = cum5*10000/count
                field_array_ls8.swir1[0][j][i] = cum6*10000/count
                field_array_ls8.swir2[0][j][i] = cum7*10000/count

    return field_array_ls8
