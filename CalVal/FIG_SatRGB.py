import DEAPlotting
import matplotlib.pyplot as plt


#
### FIGURE 
#
# Plot RGB array for satellite data
#
def FIG_sat_RGB(sat_array, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    
    if field_data[3] == 'Landsat8':
        DEAPlotting.three_band_image(sat_array, bands = ['red', 'green', 'blue'], time = 0, contrast_enhance=False)
    elif field_data[3] == 'Sentinel':
        DEAPlotting.three_band_image(sat_array, bands = ['nbar_red', 'nbar_green', 'nbar_blue'], time = 0, contrast_enhance=False)
    else:
        print('Satellite name should be one of Landsat8 or Sentinel. I got', field_data[3])

    plt.title(fig_title+': RGB colours', fontweight='bold')
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_Satellite_RGB.png')
