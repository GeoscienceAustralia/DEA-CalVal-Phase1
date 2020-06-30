import numpy as np


#
# ### Create Field full band xarray
#
# The field xarray is based on the pixel locations of the satellite data, where
# each pixel contains an average of all field data measurements that fall
# within the pixel.
#
def create_field_from_sat(ls_sat_array, s2_sat_array, ls_ground_brdf, s2_ground_brdf, ls_xloc, s2_xloc, field_data):

    ls_field_array = ls_sat_array.astype(float)
    s2_field_array = s2_sat_array.astype(float)

    #
    # Test for Collection 6 upgrade. If so, set the half pixel size to 15m, otherwise 12.5m
    #
    try:
        if field_data[7] == 'C6':
            halfpix = 15.0
        else:
            halfpix = 12.5

    except IndexError:
        halfpix = 12.5

    for i in range(len(ls_sat_array.x)):
        for j in range(len(ls_sat_array.y)):
            count = 0
            cum1, cum2, cum3, cum4, cum5, cum6, cum7 = 0,0,0,0,0,0,0
            for k in range(len(ls_xloc)):
                if (ls_sat_array.x[i]-halfpix < ls_xloc[k][0] < ls_sat_array.x[i]+halfpix) and (ls_sat_array.y[j]-halfpix < ls_xloc[k][1] < ls_sat_array.y[j]+halfpix):
                    cum1 = cum1+ls_ground_brdf.iloc[k]['band1']
                    cum2 = cum2+ls_ground_brdf.iloc[k]['band2']
                    cum3 = cum3+ls_ground_brdf.iloc[k]['band3']
                    cum4 = cum4+ls_ground_brdf.iloc[k]['band4']
                    cum5 = cum5+ls_ground_brdf.iloc[k]['band5']
                    cum6 = cum6+ls_ground_brdf.iloc[k]['band6']
                    cum7 = cum7+ls_ground_brdf.iloc[k]['band7']
                    count=count+1
            if count < 1:
                ls_field_array.coastal_aerosol[0][j][i] = np.nan
                ls_field_array.blue[0][j][i] = np.nan
                ls_field_array.green[0][j][i] = np.nan
                ls_field_array.red[0][j][i] = np.nan
                ls_field_array.nir[0][j][i] = np.nan
                ls_field_array.swir1[0][j][i] = np.nan
                ls_field_array.swir2[0][j][i] = np.nan
            else:
                ls_field_array.coastal_aerosol[0][j][i] = cum1*10000/count            
                ls_field_array.blue[0][j][i] = cum2*10000/count
                ls_field_array.green[0][j][i] = cum3*10000/count
                ls_field_array.red[0][j][i] = cum4*10000/count
                ls_field_array.nir[0][j][i] = cum5*10000/count
                ls_field_array.swir1[0][j][i] = cum6*10000/count
                ls_field_array.swir2[0][j][i] = cum7*10000/count

    if s2_sat_array.notnull():
        for i in range(len(s2_sat_array.x)):
            for j in range(len(s2_sat_array.y)):
                count = 0
                cum1, cum2, cum3, cum4, cum5, cum6, cum7, cum8, cum8a, cum11, cum12 = 0,0,0,0,0,0,0,0,0,0,0
                for k in range(len(s2_xloc)):
                    if (s2_sat_array.x[i]-5.0 < s2_xloc[k][0] < s2_sat_array.x[i]+5.0) and (s2_sat_array.y[j]-5.0 < s2_xloc[k][1] < s2_sat_array.y[j]+5.0):
                        cum1 = cum1+s2_ground_brdf.iloc[k]['band1']
                        cum2 = cum2+s2_ground_brdf.iloc[k]['band2']
                        cum3 = cum3+s2_ground_brdf.iloc[k]['band3']
                        cum4 = cum4+s2_ground_brdf.iloc[k]['band4']
                        cum5 = cum5+s2_ground_brdf.iloc[k]['band5']
                        cum6 = cum6+s2_ground_brdf.iloc[k]['band6']
                        cum7 = cum7+s2_ground_brdf.iloc[k]['band7']
                        cum8 = cum8+s2_ground_brdf.iloc[k]['band8']
                        cum8a = cum8a+s2_ground_brdf.iloc[k]['band8a']
                        cum11 = cum11+s2_ground_brdf.iloc[k]['band11']
                        cum12 = cum12+s2_ground_brdf.iloc[k]['band12']
                        count=count+1
                if count < 1:
                    s2_field_array.nbart_coastal_aerosol[0][j][i] = np.nan
                    s2_field_array.nbart_blue[0][j][i] = np.nan
                    s2_field_array.nbart_green[0][j][i] = np.nan
                    s2_field_array.nbart_red[0][j][i] = np.nan
                    s2_field_array.nbart_red_edge_1[0][j][i] = np.nan
                    s2_field_array.nbart_red_edge_2[0][j][i] = np.nan
                    s2_field_array.nbart_red_edge_3[0][j][i] = np.nan
                    s2_field_array.nbart_nir_1[0][j][i] = np.nan
                    s2_field_array.nbart_nir_2[0][j][i] = np.nan
                    s2_field_array.nbart_swir_2[0][j][i] = np.nan
                    s2_field_array.nbart_swir_3[0][j][i] = np.nan
                else:
                    s2_field_array.nbart_coastal_aerosol[0][j][i] = cum1*10000/count            
                    s2_field_array.nbart_blue[0][j][i] = cum2*10000/count
                    s2_field_array.nbart_green[0][j][i] = cum3*10000/count
                    s2_field_array.nbart_red[0][j][i] = cum4*10000/count
                    s2_field_array.nbart_red_edge_1[0][j][i] = cum5*10000/count
                    s2_field_array.nbart_red_edge_2[0][j][i] = cum6*10000/count
                    s2_field_array.nbart_red_edge_3[0][j][i] = cum7*10000/count
                    s2_field_array.nbart_nir_1[0][j][i] = cum8*10000/count
                    s2_field_array.nbart_nir_2[0][j][i] = cum8a*10000/count
                    s2_field_array.nbart_swir_2[0][j][i] = cum11*10000/count
                    s2_field_array.nbart_swir_3[0][j][i] = cum12*10000/count

    return ls_field_array, s2_field_array                
