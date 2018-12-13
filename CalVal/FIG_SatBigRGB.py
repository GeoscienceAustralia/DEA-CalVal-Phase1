import DEAPlotting
import matplotlib.pyplot as plt
import matplotlib.patches as patches


#
### FIGURE 
#
# Plot large-area context RGB array for satellite data
#
def FIG_sat_bigRGB(sat_array, sat_bigarray, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]

    if field_data[3] == 'Landsat8':
        fig, axes = DEAPlotting.three_band_image(sat_bigarray, bands = ['red', 'green', 'blue'], time = 0, title='', contrast_enhance=False)
    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        fig, axes = DEAPlotting.three_band_image(sat_bigarray, bands = ['nbart_red', 'nbart_green', 'nbart_blue'], time = 0, title='', contrast_enhance=False)
    else:
        print('Satellite name must be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    rect = patches.Rectangle((float(sat_array.x.min()),float(sat_array.y.min())), 100, 100, angle=0.0, fill=False, color='white', lw = 2.5)
    rect2 = patches.Rectangle((float(sat_array.x.min()),float(sat_array.y.min())), 100, 100, angle=0.0, fill=False, color='black', lw = 1)
    axes.add_patch(rect)
    axes.add_patch(rect2)

    #plt.title(fig_title+': Large Area Context: RGB colours', fontweight='bold')

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_Satellite_bigRGB.png', dpi=300)
