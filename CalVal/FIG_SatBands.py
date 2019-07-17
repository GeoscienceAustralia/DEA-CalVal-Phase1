import matplotlib.pyplot as plt
import numpy as np


#
## Figure 
#
### Plot Satellite arrays for each band
#
# Each panel shows the satellite data.
#
def FIG_sat_bands(sat_array, field_array, output, field_data, fignum):

    newarr = sat_array/sat_array.mean()
    newarr = newarr.reset_index('time', drop=True)

    subsat_array = sat_array.where(field_array*0 == 0)
    dummy = subsat_array.std()/subsat_array.mean()*100
    variance = dummy.copy()
    dummin = min(dummy.values())
    dummax = max(dummy.values())
    dummean = np.mean(dummy.to_array())

    #fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(11.5, 9.5))
    #fig.suptitle(fig_title+': Satellite reflectances\nVariances: max='+str(format(dummax.values, '.1f'))+'%, min='+str(format(dummin.values, '.1f'))+'%, mean='+str(format(dummean.values, '.1f'))+'%', fontweight='bold')
    plt.tight_layout(pad=5.5, w_pad=4.5, h_pad=2.5)

    #
    # Set levels from 0.8 to 1.2, inclusive, with a step of 0.01
    #
    levels = []
    for i in range(80, 121, 1):
        levels.append(i/100)

    if field_data[3] == 'Landsat8':
        newarr.coastal_aerosol.plot(ax=axes[0,0], levels=levels)
        newarr.blue.plot(ax=axes[0,1], levels=levels)
        newarr.green.plot(ax=axes[0,2], levels=levels)
        newarr.red.plot(ax=axes[1,0], levels=levels)
        newarr.nir.plot(ax=axes[1,1], levels=levels)
        newarr.swir1.plot(ax=axes[1,2], levels=levels)
        newarr.swir2.plot(ax=axes[2,0], levels=levels)
        axes[2,1].axis('off')
        axes[2,2].axis('off')
        axes[3,0].axis('off')
        axes[3,1].axis('off')
        axes[3,2].axis('off')
    
    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        newarr.nbart_coastal_aerosol.plot(ax=axes[0,0], levels=levels)
        newarr.nbart_blue.plot(ax=axes[0,1], levels=levels)
        newarr.nbart_green.plot(ax=axes[0,2], levels=levels)
        newarr.nbart_red.plot(ax=axes[1,0], levels=levels)
        newarr.nbart_red_edge_1.plot(ax=axes[1,1], levels=levels)
        newarr.nbart_red_edge_2.plot(ax=axes[1,2], levels=levels)
        newarr.nbart_red_edge_3.plot(ax=axes[2,0], levels=levels)
        newarr.nbart_nir_1.plot(ax=axes[2,1], levels=levels)
        newarr.nbart_nir_2.plot(ax=axes[2,2], levels=levels)
        newarr.nbart_swir_2.plot(ax=axes[3,0], levels=levels)
        newarr.nbart_swir_3.plot(ax=axes[3,1], levels=levels)
        axes[3,2].axis('off')

    else:
        print('Satellite name should be one of Landsat8 or Sentinel2a/b. I got', field_data[3])

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_SatBands.png')

    return variance
