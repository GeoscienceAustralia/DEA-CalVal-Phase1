import matplotlib.pyplot as plt

#
## Figure 
#
### Plot timelines for GOOD panel and ground data, with one line in one panel
#
def FIG_good_timelines(gpta, gpt, adt, panel_plot_layout, multi_timeline_plot, output, field_data, fignum):
    n, m = panel_plot_layout(len(gpta.Line.unique()))

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=m, ncols=n, figsize=(6.0, 4.0))
    #fig.suptitle(fig_title+': Time Stamps for each line, including GOOD data', fontweight='bold')
    plt.tight_layout(pad=1.5, w_pad=-2.0, h_pad=0.0)

    multi_timeline_plot(n, m, gpt, adt, axes)

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_GoodTimeLineData.png', dpi=300)
