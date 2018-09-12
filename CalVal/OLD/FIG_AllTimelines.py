import matplotlib.pyplot as plt


#
### Create multi-panel plot function with one line plotted on each panel
#
# Given the number of lines in the dataset, determine the best plot layout.
# This assumes a single column for only a single plot,
# two columns for up to four panel plots and three columns for up to
# 15 panel plots.
#
# Panel readings are coded in as blue crosses and ground readings are
# coded as orange vertical lines.
#
def panel_plot_layout(nlines):
    n=3; m=5
    if nlines < 13:
        m=4
    if nlines < 10:
        m=3
    if nlines < 9:
        n=2; m=4
    if nlines < 7:
        m=3
    if nlines < 5:
        m=2
    if nlines < 3:
        m=1
    if nlines < 2:
        n=1
    return n, m


def multi_timeline_plot(n, m, gpta, adta, axes):
    for i in range(m):
        for j in range(n):

            k = (n*i)+j+1   # Panel number

            if gpta[(gpta['Line']==k)].empty:
                axes[i,j].axis('off')

            else:
                temp_loop = gpta[(gpta['Line']==k)].astype(float)
                all_loop = adta[(adta['Line']==k)].astype(float)
                all_loop.plot(x='date_saved', y='ones', kind='scatter', legend=False, ax=axes[i,j], color='orange', marker='|')
                temp_loop.plot(x='date_saved', y='ones', kind='scatter', legend=False, ax=axes[i,j], marker='x', sharey=True, title='line'+str(k))
                if i==m-1:
                    axes[i,j].set_xlabel("Time (seconds)")
                else:
                    axes[i,j].set_xlabel("")
                axes[i,j].set_ylabel("")
                axes[i,j].set_yticks([])
    
    if k in [1, 3, 5, 7, 11, 14]:
        axes[-1, -1].axis('off')
    if k in [10, 13]:
        axes[-1, -1].axis('off')
        axes[-1, -2].axis('off')

#
## Figure 
#
### Plot timelines for ALL panel and ground data, with one line in one panel
#
def FIG_all_timelines(gpta, adta, output, field_data, fignum):

    n, m = panel_plot_layout(len(gpta.Line.unique()))

    fig_title = 'Figure '+str(fignum)+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' '+field_data[3]
    fig, axes = plt.subplots(nrows=m, ncols=n, figsize=(11.5, 9.5))
    fig.suptitle(fig_title+': Time Stamps for each line, including ALL data', fontweight='bold')
    plt.tight_layout(pad=4.5, w_pad=1.0, h_pad=2.5)

    multi_timeline_plot(n, m, gpta, adta, axes)

    plt.savefig(output+field_data[0]+'_'+field_data[1]+'_'+field_data[2]+'_'+field_data[3]+'_'+'Fig'+str(fignum)+'_AllTimeLineData.png')
