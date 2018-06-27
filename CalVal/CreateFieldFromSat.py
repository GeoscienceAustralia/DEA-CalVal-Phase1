import numpy as np


#
# ### Create Field full band xarray
#
# The field xarray is based on the pixel locations of the satellite data, where
# each pixel contains an average of all field data measurements that fall
# within the pixel.
#
def create_field_from_sat(sat_array, ground_brdf, xloc):
    field_array = sat_array.astype(float)

    for i in range(len(sat_array.x)):
        for j in range(len(sat_array.y)):
            count = 0
            cum1, cum2, cum3, cum4, cum5, cum6, cum7 = 0,0,0,0,0,0,0
            for k in range(len(xloc)):
                if (sat_array.x[i]-12.5 < xloc[k][0] < sat_array.x[i]+12.5) and (sat_array.y[j]-12.5 < xloc[k][1] < sat_array.y[j]+12.5):
                    cum1 = cum1+ground_brdf.iloc[k]['band1']
                    cum2 = cum2+ground_brdf.iloc[k]['band2']
                    cum3 = cum3+ground_brdf.iloc[k]['band3']
                    cum4 = cum4+ground_brdf.iloc[k]['band4']
                    cum5 = cum5+ground_brdf.iloc[k]['band5']
                    cum6 = cum6+ground_brdf.iloc[k]['band6']
                    cum7 = cum7+ground_brdf.iloc[k]['band7']
                    count=count+1
            if count<10:
                field_array.coastal_aerosol[0][j][i] = np.nan
                field_array.blue[0][j][i] = np.nan
                field_array.green[0][j][i] = np.nan
                field_array.red[0][j][i] = np.nan
                field_array.nir[0][j][i] = np.nan
                field_array.swir1[0][j][i] = np.nan
                field_array.swir2[0][j][i] = np.nan
            else:
                field_array.coastal_aerosol[0][j][i] = cum1*10000/count            
                field_array.blue[0][j][i] = cum2*10000/count
                field_array.green[0][j][i] = cum3*10000/count
                field_array.red[0][j][i] = cum4*10000/count
                field_array.nir[0][j][i] = cum5*10000/count
                field_array.swir1[0][j][i] = cum6*10000/count
                field_array.swir2[0][j][i] = cum7*10000/count
    return field_array                
