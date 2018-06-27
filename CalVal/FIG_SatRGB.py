import DEAPlotting
import matplotlib.pyplot as plt


#
### FIGURE 
#
# Plot RGB array for satellite data
#
def FIG_sat_RGB(sat_array, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    DEAPlotting.three_band_image(sat_array, bands = ['red', 'green', 'blue'], time = 0, contrast_enhance=False)

    plt.title(fig_title+': RGB colours', fontweight='bold')
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_Satellite_RGB.png')
