import os, shutil

import matplotlib.pyplot as plt


#
## Figure
### Plot panel radiances for all/good/bad panels
#
def FIG_panel_radiances(good_panel_spec, bad_panel_spec, all_panel_spec, output, field_data, fignum):

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(11.0, 5.0))
    #fig.suptitle(fig_title, fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    #
    # Plot the radiances for the good panels.
    #
    good_panel_spec.plot(title = 'Good panel radiances', legend=False, ax=axes[0])
    axes[0].set_ylabel("Radiance")

    #
    # Plot the bad panel radiances, if they exist
    #
    try:
        bad_panel_spec.plot(title = "Bad panel radiances", legend=False, ax=axes[1])
    except AttributeError:
        pass
    #
    # Plot the ALL panel radiances
    #
    all_panel_spec.plot(title = " All panel radiances", legend=False, ax=axes[2])

    #
    # Remove old files in directory and create a new one
    #
    directory = os.path.dirname(output)
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.makedirs(directory)

    #
    # Save plot to output directory.
    #
    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_PanelRadiances.png')
    
