import DEAPlotting
import matplotlib.pyplot as plt

#import importlib
#importlib.reload(DEAPlotting)

#
### FIGURE 
#
# Plot large-area context RGB array for satellite data
#
def FIG_many_S2ARGB(s2a_bigarray, output, field_data, fignum):

    print('Sentinel 2a')
    DEAPlotting.three_band_image_subplots(s2a_bigarray, bands = ['nbart_red', 'nbart_green', 'nbart_blue'], num_cols=8, figsize = (18, 45), contrast_enhance=False)
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_Satellite_bigRGB_S2a.png')
