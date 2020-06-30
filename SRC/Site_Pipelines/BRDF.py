import pandas as pd
import math


#
# BRDF CALCULATION
#

def ReadAndCalc(brdf_data, ls_ground_bands, s2_ground_bands, field_data):

    hb = 2 # set to emulate spherical crowns that are separated from the
    br = 1 # ground by half their diameter

    pib = math.pi/180 # convert from degrees to radians

    n_factor = 1

    #
    # Create pandas dataframe "brdf_df" which contains the BRDF values
    # for seven LS8 bands
    #   
    brdf_df = pd.DataFrame(data=brdf_data[1:,1:],
                  index=brdf_data[1:,0],
                  columns=brdf_data[0,1:])

    s2_brdf_df = brdf_df.copy()
    ls_brdf_df = brdf_df.copy()

    ls_brdf_df.drop(['band5', 'band6', 'band7', 'band8a'], inplace=True)
    ls_brdf_df.rename({'band11': 'band6', 'band12': 'band7', 'band8': 'band5'}, axis='index', inplace=True)
    ls_brdf_df.reindex(['band1', 'band2', 'band3', 'band4', 'band5', 'band6', 'band7'])

    ls_ground_brdf = ls_ground_bands.copy()
    s2_ground_brdf = s2_ground_bands.copy()

    #
    # Landsat 8
    #
    for i in ls_ground_bands.index:
        for j in ls_brdf_df.index:
            norm_1 = float(ls_brdf_df.loc[j,'brdf1'])/float(ls_brdf_df.loc[j,'brdf0'])
            norm_2 = float(ls_brdf_df.loc[j,'brdf2'])/float(ls_brdf_df.loc[j,'brdf0'])
            solar_angle = ls_ground_bands.loc[i,'Solar_angle']
            rland = ls_ground_bands.loc[i,j]
    
            if n_factor == 0:
                fnn = 1
            else:
                fnn = RL_brdf(45*pib, 0, 0, hb, br, 1, norm_1, norm_2)

            solar = solar_angle*pib

            ann = RL_brdf(solar, 0, 0, hb, br, 1, norm_1, norm_2)
            ref = rland * fnn / ann
            ls_ground_brdf.loc[i,j] = ref

    #
    # Sentinel 2
    #
    for i in s2_ground_bands.index:
        for j in s2_brdf_df.index:
            norm_1 = float(s2_brdf_df.loc[j,'brdf1'])/float(s2_brdf_df.loc[j,'brdf0'])
            norm_2 = float(s2_brdf_df.loc[j,'brdf2'])/float(s2_brdf_df.loc[j,'brdf0'])
            solar_angle = s2_ground_bands.loc[i,'Solar_angle']
            rland = s2_ground_bands.loc[i,j]
    
            if n_factor == 0:
                fnn = 1
            else:
                fnn = RL_brdf(45*pib, 0, 0, hb, br, 1, norm_1, norm_2)

            solar = solar_angle*pib

            ann = RL_brdf(solar, 0, 0, hb, br, 1, norm_1, norm_2)
            ref = rland * fnn / ann
            s2_ground_brdf.loc[i,j] = ref

    return ls_ground_brdf, s2_ground_brdf, hb, br

#
#
#
def RL_brdf(solar, view, ra, hb, br, brdf0, brdf1, brdf2):
    cossolar = math.cos(solar)
    cosvia = math.cos(view)
    cosra = math.cos(ra)
    sinsolar = math.sin(solar)
    sinvia = math.sin(view)
    sinra = math.sin(ra)
    
    cosxi = (cossolar * cosvia) + (sinsolar * sinvia * cosra) # (43)
    
    if cosxi >= 1:
        cosxi = 1
    
    xi = math.acos(cosxi)
    
    rs_thick = (((((math.pi/2) - xi) * math.cos(xi)) + math.sin(xi)) / (cossolar \
                    + cosvia)) - (math.pi/4)  # (38)
    
    tansolar = sinsolar / cossolar
    tanvia = sinvia / cosvia
    theta_new_v = math.atan(br * tanvia)      # (44)
    theta_new_s = math.atan(br * tansolar)    # (44)
    
    cosxi = (math.cos(theta_new_s) * math.cos(theta_new_v)) + (math.sin(theta_new_s) \
             * math.sin(theta_new_v) * cosra) # (43)
    
    if cosxi >= 1:
        cosxi = 1
    
    secsolar = 1 / math.cos(theta_new_s)
    secvia = 1 / math.cos(theta_new_v)
    
    d_li2 = abs(math.tan(theta_new_s)**2 + math.tan(theta_new_v)**2 - (2 * \
                math.tan(theta_new_s)*math.tan(theta_new_v)*cosra)) # (42)**2
    
    x_li = math.tan(theta_new_s) * math.tan(theta_new_v) * sinra
    cosl = hb * math.sqrt(d_li2 + x_li**2) / (secsolar + secvia) # (41)
    
    if cosl >= 1:
        o_li = 0
    else:
        l_li=math.acos(cosl)
        o_li = (l_li - (math.sin(l_li) * math.cos(l_li))) * (secsolar + secvia) \
                / math.pi     # (40)
    
    li_sparse = o_li - (secsolar + secvia) + (0.5 * (1 + cosxi) * secsolar \
                * secvia)  # (39)
    
    rl_brdf = brdf0 + (brdf1 * rs_thick) + (brdf2 * li_sparse)  # (37)
    return rl_brdf
