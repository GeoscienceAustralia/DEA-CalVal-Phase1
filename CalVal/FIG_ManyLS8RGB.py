import DEAPlotting
import matplotlib.pyplot as plt

#import importlib
#importlib.reload(DEAPlotting)

#
### FIGURE 
#
# Plot large-area context RGB array for satellite data
#
def FIG_many_LS8RGB(ls8_bigarray, output, field_data, fignum):

    print('Landsat 8')
    DEAPlotting.three_band_image_subplots(ls8_bigarray, bands = ['red', 'green', 'blue'], num_cols=8, figsize = (18, 65), contrast_enhance=False)
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_Satellite_bigRGB_LS8.png')
