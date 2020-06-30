import DEAPlotting
import matplotlib.pyplot as plt

#import importlib
#importlib.reload(DEAPlotting)

#
### FIGURE 
#
# Plot large-area context RGB array for satellite data
#
def FIG_many_S2BRGB(s2b_bigarray, output, field_data, fignum):

    print('Sentinel 2b')
    DEAPlotting.three_band_image_subplots(s2b_bigarray, bands = ['nbart_red', 'nbart_green', 'nbart_blue'], num_cols=4, figsize = (18, 25), contrast_enhance=False)
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_Satellite_bigRGB_S2b.png')

