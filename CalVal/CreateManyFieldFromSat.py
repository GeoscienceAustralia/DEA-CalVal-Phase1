import numpy as np


#
# ### Create Field full band xarray
#
# The field xarray is based on the pixel locations of the satellite data, where
# each pixel contains an average of all field data measurements that fall
# within the pixel.
#
def create_many_field_from_sat(ls8_array, s2a_array, ground_brdf_ls8, ground_brdf_s2a, xloc):

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

    ############
    # Sentinel #
    ############

    halfpix = 5.0
    field_array_s2a = s2a_array.astype(float)
    for i in range(len(s2a_array.x)):
        for j in range(len(s2a_array.y)):
            count = 0
            cum1, cum2, cum3, cum4, cum5, cum6, cum7, cum8, cum8a, cum11, cum12 = 0,0,0,0,0,0,0,0,0,0,0
            for k in range(len(xloc)):
                if (s2a_array.x[i]-halfpix < xloc[k][0] < s2a_array.x[i]+halfpix) and (s2a_array.y[j]-halfpix < xloc[k][1] < s2a_array.y[j]+halfpix):
                    cum1 = cum1+ground_brdf_s2a.iloc[k]['band1']
                    cum2 = cum2+ground_brdf_s2a.iloc[k]['band2']
                    cum3 = cum3+ground_brdf_s2a.iloc[k]['band3']
                    cum4 = cum4+ground_brdf_s2a.iloc[k]['band4']
                    cum5 = cum5+ground_brdf_s2a.iloc[k]['band5']
                    cum6 = cum6+ground_brdf_s2a.iloc[k]['band6']
                    cum7 = cum7+ground_brdf_s2a.iloc[k]['band7']
                    cum8 = cum8+ground_brdf_s2a.iloc[k]['band8']
                    cum8a = cum8a+ground_brdf_s2a.iloc[k]['band8a']
                    cum11 = cum11+ground_brdf_s2a.iloc[k]['band11']
                    cum12 = cum12+ground_brdf_s2a.iloc[k]['band12']
                    count=count+1
            if count < 1:
                field_array_s2a.nbar_coastal_aerosol[0][j][i] = np.nan
                field_array_s2a.nbar_blue[0][j][i] = np.nan
                field_array_s2a.nbar_green[0][j][i] = np.nan
                field_array_s2a.nbar_red[0][j][i] = np.nan
                field_array_s2a.nbar_red_edge_1[0][j][i] = np.nan
                field_array_s2a.nbar_red_edge_2[0][j][i] = np.nan
                field_array_s2a.nbar_red_edge_3[0][j][i] = np.nan
                field_array_s2a.nbar_nir_1[0][j][i] = np.nan
                field_array_s2a.nbar_nir_2[0][j][i] = np.nan
                field_array_s2a.nbar_swir_2[0][j][i] = np.nan
                field_array_s2a.nbar_swir_3[0][j][i] = np.nan
            else:
                field_array_s2a.nbar_coastal_aerosol[0][j][i] = cum1*10000/count            
                field_array_s2a.nbar_blue[0][j][i] = cum2*10000/count
                field_array_s2a.nbar_green[0][j][i] = cum3*10000/count
                field_array_s2a.nbar_red[0][j][i] = cum4*10000/count
                field_array_s2a.nbar_red_edge_1[0][j][i] = cum5*10000/count
                field_array_s2a.nbar_red_edge_2[0][j][i] = cum6*10000/count
                field_array_s2a.nbar_red_edge_3[0][j][i] = cum7*10000/count
                field_array_s2a.nbar_nir_1[0][j][i] = cum8*10000/count
                field_array_s2a.nbar_nir_2[0][j][i] = cum8a*10000/count
                field_array_s2a.nbar_swir_2[0][j][i] = cum11*10000/count
                field_array_s2a.nbar_swir_3[0][j][i] = cum12*10000/count


    return field_array_ls8, field_array_s2a                
