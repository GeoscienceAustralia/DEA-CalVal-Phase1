from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import csv, glob, sys, os, re
import math
import pyproj

import datacube
import DEAPlotting
import matplotlib.pyplot as plt


#
# Action functions are defined to retrieve specific parts of the header for each
# spectrum. These functions are used in extract_metadata.
#

# Instrument Number
def action1(l):
    return l[27:34]

# Datetime of spectrum
def action2(l):
    return l[16:38]

# SWIR1 gain
def action3(l):
    return l[15:33]

# SWIR2 gain
def action4(l):
    return l[15:33]

# GPS Latitude in decimal degrees
def action5(l):
    return float(l[17:20])-float(l[20:27])/60

# GPS Longitude in decimal degrees
def action6(l):
    return float(l[19:22])+float(l[22:30])/60

#
# Based on action functions defined above, extract header metadata from
# a file.
#
def extract_metadata(filename):
    strings = {
        'instrument number': action1,
        'Spectrum saved': action2,
        'SWIR1 gain': action3,
        'SWIR2 gain': action4,
        'GPS-Latitude': action5,
        'GPS-Longitude': action6
    }
    
    with open(filename) as file:
        list_of_actions = []
        for line in file:
            for search, action in strings.items():
                if search in line:
                    list_of_actions.append(action(line))
        return list_of_actions

#
### Extract spectrum and header information from a spectrum file. 
### Create a Pandas dataframe with the result.
#
def load_spectrum_to_df(infile, li):
    
    inst, date_str, swir1_go, swir2_go, lat, lon = extract_metadata(infile)

    swir1_gain = swir1_go[:3]
    swir1_offset = swir1_go[-4:]
    swir2_gain = swir2_go[:3]
    swir2_offset = swir2_go[-4:]

    date_saved = datetime.strptime(date_str, '%m/%d/%Y at %H:%M:%S')
    
    df = pd.read_csv(infile, skiprows=38, delim_whitespace=True)
    filename = df.columns[1]
    df.rename({filename: 'radiance'}, axis=1, inplace=True)
    df['filename'] = filename
    df['date_saved'] = date_saved
    df['Latitude'] = lat
    df['Longitude'] = lon
    df['Line'] = li
    df['Spec_number'] = int(filename[-10:-8])
    df['Inst_number'] = inst
    df['SWIR1_gain'] = swir1_gain
    df['SWIR1_offset'] = swir1_offset
    df['SWIR2_gain'] = swir2_gain
    df['SWIR2_offset'] = swir2_offset
    return df


#
### Loop through all spectrum files in "indir" and combine the resulting dataframes.
#
# For each 'line*' directory in 'indir', iterate through each file
# ending with 'suffix' and run 'load_spectrum_to_df'. Finally,
# return a concatenated dataframe made up of all the individual
# dataframes.
#
def load_from_dir(indir, suffix):
    all_dfs = []
    for li in range(1, len(glob.glob(indir+'line*'))+1):
        home2 = indir+'line'+str(li)+'/'

        #
        # Initalise 'spectra' list and fill with files that end in 'suffix'
        #
        spectra = []
        for root, dirs, files in sorted(os.walk(home2)):
            for file in files:
                if file.endswith(suffix):
                    spectra.append(file)
        spectra = sorted(spectra)

        for name in spectra:
            infile = home2 + name

            df = load_spectrum_to_df(infile, li)
            all_dfs.append(df)
    return pd.concat(all_dfs)

#
###Specify which spectra are panels/ground/good/bad
#
# Determine panel file names by assuming that all panels have a data value of
# at least 0.06 in the first wavelength (350nm). Call this dataframe 'panel_names'.
#
#   good_panels = all panel data with bad panels removed
#   bad_panels = all bad panel data
#   all_panels = both good and bad panel data
#   good_grounds = good ground readings
#   all_grounds = all ground data.
#
# Any bad ground data (bad_grounds) is defined in the 2nd cell.
#
def extract_panels_grounds(alldata, bad_pans, bad_grounds):
    panel_names = alldata[(alldata['Wavelength']==350) & (alldata['radiance']>=0.06)]['filename']

    all_panels = alldata.loc[alldata['filename'].isin(panel_names)]
    good_panels = all_panels.loc[~all_panels['filename'].isin(bad_pans)]
    bad_panels = alldata.loc[alldata['filename'].isin(bad_pans)]

    tmp_grounds = alldata.loc[~alldata['filename'].isin(bad_grounds)]
    good_grounds = tmp_grounds.loc[~tmp_grounds['filename'].isin(panel_names)]
    all_grounds = alldata.loc[~alldata['filename'].isin(panel_names)]
    
    return panel_names, all_panels, good_panels, bad_panels, good_grounds, all_grounds


#
### Make a dataframe that contains just the spectra, with one spectrum per column
#
# Loop over each line 'i' and then over each spectrum 'j' within line 'i'.
# 
# For the first spectrum, copy both the
# Wavelength (for the index) and radiance to a new dataframe (temp2).
# For all subsequent spectra, append the new dataframe with a radiance
# column. The results in a new dataframe 'outpanel' that has a wavelength
# column (also set as the index), plus all the radiances in subsequent
# columns.
#
def make_spec_df(in_df):
    for i in in_df.Line.unique():
        temp_loop = in_df[(in_df['Wavelength']==350) & (in_df['Line']==i)]
        for j in temp_loop['Spec_number']:
            temp2 = in_df[(in_df['Spec_number']==j) & (in_df['Line']==i)]
            
            try:
                out_df['radiance'+str(i)+"-"+str(j)] = temp2['radiance']
            except UnboundLocalError:
                out_df = temp2[['Wavelength', 'radiance']].copy()

    out_df.set_index("Wavelength", inplace=True)

    return out_df

#
## Figure 1
### Plot panel radiances for all/good/bad panels
#
def FIG_panel_radiances(good_panel_spec, bad_panel_spec, all_panel_spec, output, field_data):

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(11.0, 5.0))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2], fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    #
    # Plot the radiances for the good panels.
    #
    good_panel_spec.plot(title = 'Good panel radiances', legend=False, ax=axes[0])
    axes[0].set_ylabel("Radiance")

    #
    # Plot the bad panel radiances, if they exist (found in line 8)
    #
    try:
        bad_panel_spec.plot(title = "Bad panel radiances", legend=False, ax=axes[1])
    except NameError:
        pass
    #
    # Plot the ALL panel radiances
    #
    all_panel_spec.plot(title = " All panel radiances", legend=False, ax=axes[2])

    #
    # Check that output directory exists, if not, create it.
    #
    directory = os.path.dirname(output)
    if not os.path.exists(directory):
        os.makedirs(directory)

    #
    # Save plot to output directory.
    #
    plt.savefig(output+'Fig01_PanelRadiances.png')
    
#
## Figure 2
#
### Diagnosis plots of bad panel spectra
#
# Create a mean of the good panel readings, as well as the bad panel
# readings. Then a ratio and a difference of the two can be (seperately)
# created and plotted.
#
# Since the two bad panel readings are higher than they should be, we
# put the bad panels on the top of the division and first in the
# difference.
#
def FIG_bad_panel_analysis(good_panel_spec, bad_panel_spec, field_data):

    good_panel_mean = good_panel_spec.mean(axis=1)

    try: 
        bad_panel_mean = bad_panel_spec.mean(axis=1)
        good_bad_div = bad_panel_mean.div(good_panel_mean, axis=0)
        good_bad_diff = bad_panel_mean.sub(good_panel_mean, axis=0)

        pd.Series.to_frame(good_bad_div)
        pd.Series.to_frame(good_bad_diff)

        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(9.5, 9.5))
        fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2], fontweight='bold')

        good_bad_div.plot(title='(average bad panels / average good panels)', legend=False, ax=axes[0,0])

        good_bad_diff.plot(title='(average bad panels) - (average good panels)', legend=False, ax=axes[0,1])

        good_panel_mean.plot(title='Average good panels', legend=False, ax=axes[1,0])
        axes[1,0].set_ylabel("Radiance")
        plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

        bad_panel_mean.plot(title='Average bad panels', legend=False, ax=axes[1,1])
        plt.savefig(output+'Fig02_GoodBadPanelCompare.png')

    except NameError:
        pass
    return good_panel_mean

#
## Figure 3
#
### Plot ground spectra (all and good), normalised to the median good spectrum
#
# These plots are used to identify any ground spectra that are bogus.
#
def FIG_ground_spectra(good_grounds_spec, all_grounds_spec, field_data, output):
    good_median = good_grounds_spec.median(axis=1)
    good_norm = good_grounds_spec.div(good_median, axis=0)
    all_norm = all_grounds_spec.div(good_median, axis=0)

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9.6, 6.0))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2], fontweight='bold')
    plt.tight_layout(pad=5.5, w_pad=1.0, h_pad=1.0)

    all_norm.plot(title="All ground radiances normalised to \nthe median ground radiance", legend=False, ax=axes[0])

    good_norm.plot(title="Good ground radiances normalised to \nthe median ground radiance", legend=False, ax=axes[1])

    plt.savefig(output+'Fig03_GroundRadiances.png')
    
#
### Create dataframe with relative time stamps
#
# Make a new dataframe with time since the first good panel reading
# along the x-axis and "1" for the y-axis. This allows a plot of the
# data timeline to be made.
#
def make_timeline(in_df, good_panels):
    
    temp_df = in_df[['date_saved', 'Line']].loc[in_df['Wavelength']==350]
    gpt = good_panels[['date_saved', 'Line']].loc[good_panels['Wavelength']==350]
    
    out_df = temp_df.copy()
    for i in range(len(out_df)):
        out_df.iloc[[i], [0]]=(temp_df.iloc[i][0]-gpt.iloc[0][0]).seconds

    out_df['ones'] = np.ones(len(out_df))
    return out_df

#
### Create time-relative dataframes
#
#   gpt = good panels
#   gpta = all panels
#   adt = good grounds
#   adta = all grounds
#
def create_time_relative_dfs(good_panels, all_panels, good_grounds, all_grounds):
    
    gpt = make_timeline(good_panels, good_panels)
    gpta = make_timeline(all_panels, good_panels)
    adt = make_timeline(good_grounds, good_panels)
    adta = make_timeline(all_grounds, good_panels)
    
    return gpt, gpta, adt, adta

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
    k=0
    for i in range(m):
        for j in range(n):
            k+=1
            if k > gpta.Line.max():
                break
            elif gpta[(gpta['Line']==k)].empty:
                axes[i,j].axis('off')
            else:
                temp_loop = gpta[(gpta['Line']==k)]
                all_loop = adta[(adta['Line']==k)]
                all_loop.plot(x='date_saved', y='ones', kind='scatter', legend=False, ax=axes[i,j], color='orange', marker='|')
                temp_loop.plot(x='date_saved', y='ones', kind='scatter', legend=False, ax=axes[i,j], marker='x', sharey=True, title='line'+str(k))
                if i==m-1:
                    axes[i,j].set_xlabel("Time (seconds)")
                else:
                    axes[i,j].set_xlabel("")
                axes[i,j].set_ylabel("")
                axes[i,j].set_yticks([])
    
    if k in [2, 4, 6, 8, 12, 15]:
        axes[-1, -1].axis('off')
    if k in [11, 14]:
        axes[-1, -1].axis('off')
        axes[-1, -2].axis('off')

#
## Figure 4
#
### Plot timelines for ALL panel and ground data, with one line in one panel
#
def FIG_all_timelines(gpta, adta, output, field_data):
    n, m = panel_plot_layout(len(gpta.Line.unique()))

    fig, axes = plt.subplots(nrows=m, ncols=n, figsize=(11.5, 9.5))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+': Time Stamps for each line, including ALL data', fontweight='bold')
    plt.tight_layout(pad=4.5, w_pad=1.0, h_pad=2.5)

    multi_timeline_plot(n, m, gpta, adta, axes)


    plt.savefig(output+'Fig04_AllTimeLineData.png')
    
#
## Figure 5
#
### Plot timelines for GOOD panel and ground data, with one line in one panel
#
def FIG_good_timelines(gpta, gpt, adt, output, field_data):
    n, m = panel_plot_layout(len(gpta.Line.unique()))

    fig, axes = plt.subplots(nrows=m, ncols=n, figsize=(11.5, 9.5))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+': Time Stamps for each line, including GOOD data', fontweight='bold')
    plt.tight_layout(pad=4.5, w_pad=1.0, h_pad=2.5)

    multi_timeline_plot(n, m, gpt, adt, axes)

    plt.savefig(output+'Fig05_GoodTimeLineData.png')

#
## Figure 6
#
### Create timeline plot of averaged, normalised all/good panels
#
#    These plots are used to identify any panels that show unusually bright or
#    dark readings, which can be weeded out as bad panels.
#    
# The general shape of the curve should follow "insolation" - the changing of
# incident light due to the Sun rising/falling in the sky.
#
# The method to create the normalised mean panels is as follows:
#
#    1. A mask of the mean good panels is created that removes the wavelengths
#       that are most affected by low atmospheric transmission.
#    2. ALL/GOOD spectra are divided by the masked mean good panel spectrum to
#       make normalised spectra.
#    3. The mean values for both ALL and GOOD normalised spectra are created.
#    4. The mean values for spectra are appended to the spt and gpta dataframes.
#    5. The mean values are plotted, as a function of time, relative to the
#       first panel time stamp.
#
def normalise_spectra(good_panel_mean, good_panel_spec, all_panel_spec, gpt, gpta):
    #
    # Create a mask to avoid wavelengths where atmospheric transmission is
    # close to zero: 1350-1480nm, 1801-1966nm and >2350nm
    #
    mask1 = good_panel_mean.where(np.logical_or(good_panel_mean.index<1350, good_panel_mean.index>1480))
    mask2 = mask1.where(np.logical_or(mask1.index<1801, mask1.index>1966))

    # 1.
    mean_panel_masked = mask2.where(np.logical_or(mask2.index<2350, mask2.index>2500))

    # 2.
    good_norm_panels_masked = good_panel_spec.div(mean_panel_masked, axis=0)
    all_norm_panels_masked = all_panel_spec.div(mean_panel_masked, axis=0)

    # 3.
    good_averages_masked = good_norm_panels_masked.mean(axis=0)
    all_averages_masked = all_norm_panels_masked.mean(axis=0)

    # 4.
    gpt['Normalised_Averaged_Panels']=good_averages_masked.values
    gpta['Normalised_Averaged_Panels']=all_averages_masked.values
    
    return gpt, gpta

#
#
#
def FIG_normalised_panels_timeline(gpt, gpta, output, field_data):
    # 5.
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(9.5, 4.5))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+': Time vs Normalised, Wavelength-averaged Panels', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    gpta.plot.scatter(x='date_saved', y='Normalised_Averaged_Panels', title='All Panels', color='black', ax=axes[0])
    gpta.plot.line(x='date_saved', y='Normalised_Averaged_Panels', ax=axes[0], style='b', legend=False)
    axes[0].set_ylabel("Normalised Average Panel Radiance")
    axes[0].set_xlabel("Time (seconds)")

    gpt.plot.scatter(x='date_saved', y='Normalised_Averaged_Panels', title='Good Panels', color='black', ax=axes[1])
    gpt.plot.line(x='date_saved', y='Normalised_Averaged_Panels', ax=axes[1], style='b', legend=False)
    axes[1].set_ylabel("")
    axes[1].set_xlabel("Time (seconds)")

    plt.savefig(output+'Fig06_TimevsAvgPanels.png')

#
## Figure X7
#
### Comparison plot between expected insolation curve and normalised, averaged panels
#
### Currently, this plot is not used.
#
#good_panel_spec.sum(axis=0)
#gpt['sum']=good_panel_spec.sum(axis=0).values
#
#ax2 = gpt.plot.scatter(x='date_saved', y='sum', color='black')
#gpt.plot.line(x='date_saved', y='sum', ax=ax2, style='b', legend=False)
#plt.figtext(0.12, 0.9, sat_name+": "+field_site+" "+field_date+" "+site_number+': Time vs Wavelength-summed Panels', fontweight='bold')
#
##
## The Following dataframe assumes 26/3/2018, where meridian is at 02:07:44 (UTC) and
## that t=0 is 00:12:58, which is the UTC date stamp of the first panel reading. This dataframe
## then gives the Insolation values, as a function of seconds.
##
#sdf_dst = pd.DataFrame([[-314.0, 0.9544765503230449], [136.0, 0.960635398038314], [586.0, 0.9662590390482365],
#                        [1036.0, 0.9713789520297165], [1486.0, 0.9760229720710379], [1936.0, 0.9802156732739963],
#                        [2386.0, 0.9839786952371856], [2836.0, 0.9873310215393157]], columns=['Time', 'Insolation'])
##
## The following plot shows the same increase in panel readins, as above, but this time, two lines for
## Insolation are plotted. The blue line shows a scaled Insolation curve. The data *should* fit this curve,
## but they do not, without re-aligning the y-axis, as shown in the orange curve. The orange curve is a good
## fit to the data, but it no longer follows the Insolation curve for the time of day.
##
## The reason for this discrepancy may be because the atmospheric absorption is not taken into account. If it
## were, then this should have the effect of steepening the Insolation curve as there is more atmospheric
## absorption when the Sun is lower in the sky (earlier in the day).
##
#sdf_dst_fixed = sdf_dst.copy()
#
#sdf_dst['Insolation']*=248
#sdf_dst.plot.line(x='Time', y='Insolation', ax=ax2)
#plt.savefig(output+'Fig07_TimevsAvgPanelsInsolation.png')

#
### Define the K-factor
#
# This reads a standard file with a response curve for the detector, given an
# ideally white surface. Then "k_f" is defined for the K-factor.
def k_factor(panel_dir, in_panel):
    k_f = pd.read_csv(panel_dir + in_panel, skiprows=5, delim_whitespace=True)
    # Set index to wavelength
    k_f.set_index("Wavelength", inplace = True) 
    
    return k_f

#
### Rename the first spectrum in ALL/GOOD panels to the correct name
#
# Rather than just "radiance", it will be named something like radiance1-0
# for the zeroth spectrum in the first line, for example.
#
def spec_rename(good_panel_spec, good_grounds_spec, firstGoodLine, firstGoodPanelSpec, firstGoodGroundSpec):
    gps_new_name = 'radiance'+str(firstGoodLine)+"-"+str(firstGoodPanelSpec)
    ggs_new_name = 'radiance'+str(firstGoodLine)+"-"+str(firstGoodGroundSpec)

    good_panel_spec.rename(columns={'radiance': gps_new_name}, inplace=True)
    good_grounds_spec.rename(columns={'radiance': ggs_new_name}, inplace=True)

#
#### Create dataframe with Reflectances
#
#Loop through each Line with spectral data:
#    1. Make an average of all the panel spectra within the Line
#       (line_avg_panel).
#    2. For each ground spectrum within the Line, divide by the average panel
#       spectrum (refl_temp).
#    3. Multiply each normalised ground spectrum my the K-factor to create
#       reflectances dataframe (line_refls).
#
# Finally, combine each dataframe for reflectances within a line into a single
# dataframe (all_refls) 
#
def create_reflectances(good_panels, good_panel_spec, good_grounds_spec, k_f):
    frames = []
    for j in good_panels.Line.unique():

        # 1.
        line_name_pans = [col for col in good_panel_spec.columns if 'radiance'+str(j)+'-' in col]

        tmplist = []
        for i in line_name_pans:
            temp = good_panel_spec[i]
            tmplist.append(temp)

        tmp_df = pd.concat(tmplist, axis=1)
        line_avg_panel = tmp_df.mean(axis=1)

        # 2.
        line_name_grounds = [col for col in good_grounds_spec.columns if 'radiance'+str(j)+'-' in col]

        tmplist = []
        for i in line_name_grounds:
            temp = good_grounds_spec[i]
            tmplist.append(temp)

        tmp_df = pd.concat(tmplist, axis=1)
        refl_tmp = tmp_df.div(line_avg_panel, axis=0)

        # 3.
        line_refls = pd.np.multiply(refl_tmp, k_f)

        frames.append(line_refls)

    return pd.concat(frames, axis=1)

#
## Figure 7
#
### Plot all ground reflectances in black, plus the Line-averaged reflectances
### in colour
#
# The Line-averaged reflectances are shown in order to identify any outlying
# lines that might have been caused by bad panel spectra (for example).
#
def FIG_reflectances(good_panels, all_refls, colpac, output, field_data):
    fig, axy = plt.subplots(nrows=1, ncols=2, figsize=(13.5, 5.5))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+': Ground Reflectances.\nBlack: Individual reflectances. Colour: Average Reflectances for each line', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    maska = all_refls[np.logical_xor(all_refls.index > 1350, all_refls.index < 1480)]
    maskb = maska[np.logical_xor(maska.index > 1801, maska.index < 1966)]
    all_refls_masked = maskb[(maskb.index < 2350)]

    axy[0].set_ylabel("Reflectance")
    axy[1].set_ylim(all_refls_masked.min().min()*0.95, all_refls_masked.max().max()*1.05)

    all_refls.plot(legend=False, ax=axy[0], color='k')
    all_refls.plot(legend=False, ax=axy[1], color='k')

    for i in good_panels.Line.unique():
        rad_name = 'radiance'+str(i)
        line = all_refls.filter(like=rad_name).mean(axis=1)
        line.plot(ax=axy[0], color=colpac[i], legend=True, label='Line'+str(i))
        line.plot(ax=axy[1], color=colpac[i], legend=False, label='Line'+str(i))

    plt.savefig(output+'Fig07_Reflectances.png')
    
#
# Read in the spectral responses for each band
#
def get_spectrum_curve(f_name):
    band_n = dict() 
    key = list()
    wavelength = np.array([], dtype='float64') 
    response = np.array([], dtype='float64') 
    with open(f_name, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=' ', skipinitialspace=True)
        for row in csv_reader:
            if row[0].lower().find('band') >= 0:
                key.append(row[0].lower()+row[1])
                if wavelength.shape[0] > 0:
                    spectrum_curve = np.vstack([wavelength, response]).T
                    band_n.update({key[len(key)-2]: spectrum_curve})
                    wavelength = np.array([], dtype='float64') 
                    response = np.array([], dtype='float64') 
            else:
                wavelength = np.append(wavelength, float(row[0]))
                response = np.append(response, float(row[1]))
    spectrum_curve = np.vstack([wavelength, response]).T
    band_n.update({key[len(key)-1]: spectrum_curve})
    wavelength = np.array([], dtype='float64') 
    response = np.array([], dtype='float64') 
    return band_n 

#
# Create weight-average of spectrum for each band
#
def field_int_curve(field_data, band):
    result = np.zeros(len(band))
    i = 0
    for b in band:
        spectrum_curve = band[b]
        dom_a = max(min(spectrum_curve[:, 0]), min(field_data[:, 0]))
        dom_b = min(max(spectrum_curve[:, 0]), max(field_data[:, 0]))
        source_x = field_data[:, 1][np.where((field_data[:, 0] >= dom_a) & 
                (field_data[:, 0] <= dom_b))]
        source_y = spectrum_curve[:, 1][np.where((spectrum_curve[:, 0] >= dom_a) & 
            (spectrum_curve[:, 0] <= dom_b))]
        result[i] = sum(source_x*source_y)/sum(source_y)
        i += 1
    return result

#
# Apply weighted band responses to all reflectances
#
def apply_weights(f_name, all_refls):
    band = get_spectrum_curve(f_name)
    result = []
    wave_length = np.array(all_refls.index, dtype='float64')
    for col in all_refls.columns:
        source_x = np.vstack([wave_length, np.array(all_refls[col], dtype='float64')]).T
        result.append(field_int_curve(source_x, band))
    result_df = pd.DataFrame(result)
    result_df.columns = list(band.keys())
    return result_df, band

#
### Reformat band reflectances and apply to dataframe "ground_bands"
#
def reformat_df(good_grounds, result_df):
    gg = good_grounds[(good_grounds['Wavelength']==350)]
    gg.reset_index(drop=True, inplace=True)

    catty = pd.concat([gg,result_df], axis=1)
    ground_bands = catty.drop(['Wavelength', 'radiance'], axis=1)
    return ground_bands

#
# ### Figure 8
#
# Plot band reflectances
#
def FIG_band_reflectances(ground_bands, result_df, band, colpac, output, field_data):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(11.5, 6.5))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+': \nGround Reflectances averaged into '+field_data[3]+' Bands\n        Line Averaged                                                         Individual spectra', fontweight='bold')
    axes[0].set_ylabel("Reflectance")
    axes[0].set_xlabel("Band Number")
    axes[1].set_xlabel("Band Number")
    axes[0].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    axes[1].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    plt.tight_layout(pad=5.5, w_pad=1.0, h_pad=1.0)

    d=pd.DataFrame([[[ground_bands[j][(ground_bands['Line']==i)].mean()] for j in list(band.keys())] for i in ground_bands.Line.unique()])
    for i in d.columns:
        d[i] = d[i].str.get(0)
        d.rename(columns={i: 'band'+str(i+1)}, inplace=True)
    for i in d.index:
        d.rename(index={i: 'Line'+str(i+1)}, inplace=True)

    d.T.plot(legend=True, ax=axes[0], color=colpac)

    result_df.T.plot(legend=False, ax=axes[1])

    plt.savefig(output+'Fig08_BandReflectances.png')
    
#
# BRDF CALCULATION
#

def ReadAndCalc(brdf_data, ground_bands):

    hb = 2 # set to emulate spherical crowns that are separated from the
    br = 1 # ground by half their diameter

    pib = math.pi/180 # convert from degrees to radians

    n_factor = 1

    #
    # Create pandas dataframe "brdf_df" which contains the BRDF values
    # for six LS8 bands
    #   
    brdf_df = pd.DataFrame(data=brdf_data[1:,1:],
                  index=brdf_data[1:,0],
                  columns=brdf_data[0,1:])
    
    ground_brdf = ground_bands.copy()
    
    for i in ground_bands.index:
        for j in brdf_df.index:
            norm_1 = float(brdf_df.loc[j,'brdf1'])/float(brdf_df.loc[j,'brdf0'])
            norm_2 = float(brdf_df.loc[j,'brdf2'])/float(brdf_df.loc[j,'brdf0'])
            solar_angle = ground_bands.loc[i,'Solar_angle']
            rland = ground_bands.loc[i,j]
    
            if n_factor == 0:
                fnn = 1
            else:
                fnn = RL_brdf(45*pib, 0, 0, hb, br, 1, norm_1, norm_2)

            solar = solar_angle*pib

            ann = RL_brdf(solar, 0, 0, hb, br, 1, norm_1, norm_2)
            ref = rland * fnn / ann
            ground_brdf.loc[i,j] = ref
            #print(i,j,rland, ref)
    return ground_brdf, hb, br

#
#
#
def RL_brdf(solar, view, ra, hb, br, brdf0, brdf1, brdf2):
    cossolar = math.cos(solar)
    cosvia = math.cos(view)
    cosra = math.cos(ra)
    sinsolar = math.sin(solar)
    sinvia = math.sin(view)
    sinra = math.sin(ra)
    
    cosxi = (cossolar * cosvia) + (sinsolar * sinvia * cosra) # (43)
    
    if cosxi >= 1:
        cosxi = 1
    
    xi = math.acos(cosxi)
    
    rs_thick = (((((math.pi/2) - xi) * math.cos(xi)) + math.sin(xi)) / (cossolar \
                    + cosvia)) - (math.pi/4)  # (38)
    
    tansolar = sinsolar / cossolar
    tanvia = sinvia / cosvia
    theta_new_v = math.atan(br * tanvia)      # (44)
    theta_new_s = math.atan(br * tansolar)    # (44)
    
    cosxi = (math.cos(theta_new_s) * math.cos(theta_new_v)) + (math.sin(theta_new_s) \
             * math.sin(theta_new_v) * cosra) # (43)
    
    if cosxi >= 1:
        cosxi = 1
    
    secsolar = 1 / math.cos(theta_new_s)
    secvia = 1 / math.cos(theta_new_v)
    
    d_li2 = abs(math.tan(theta_new_s)**2 + math.tan(theta_new_v)**2 - (2 * \
                math.tan(theta_new_s)*math.tan(theta_new_v)*cosra)) # (42)**2
    
    x_li = math.tan(theta_new_s) * math.tan(theta_new_v) * sinra
    cosl = hb * math.sqrt(d_li2 + x_li**2) / (secsolar + secvia) # (41)
    
    if cosl >= 1:
        o_li = 0
    else:
        l_li=math.acos(cosl)
        o_li = (l_li - (math.sin(l_li) * math.cos(l_li))) * (secsolar + secvia) \
                / math.pi     # (40)
    
    li_sparse = o_li - (secsolar + secvia) + (0.5 * (1 + cosxi) * secsolar \
                * secvia)  # (39)
    
    rl_brdf = brdf0 + (brdf1 * rs_thick) + (brdf2 * li_sparse)  # (37)
    return rl_brdf

#
## Figure 9
#
### Plot satellite band extents against median ground spectrum
#
# This plot will show where the satellite bands fall, with respect to the
# spectrum and in particular, with respect to the atmospheric absorbtion features.
#
def FIG_band_extents(all_refls, band_min, band_max, output, field_data):
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9.5, 6.5))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+': \nMedian ground reflectance with '+field_data[3]+' Bands shown as black bars', fontweight='bold')
    axes.set_ylabel("Reflectance")
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    med = all_refls.median(axis=1)
    all_refls['Median'] = med
    all_refls.plot(y='Median', ax=axes, legend=False)

    if field_data[3] == 'Landsat 8': 
        y_cord = [0.065, 0.075, 0.08, 0.09, 0.11, 0.18, 0.15, 0.12]
    elif field_data[3] == 'Sentinel':
        y_cord = [0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.17, 0.15]
    else:
        print("Incorrect Satellite name - must be one of Landsat 8 or Sentinel")

    for i in range(len(band_min)):
        plt.annotate('', xy = (band_min[i], y_cord[i]),  xycoords = 'data', \
            xytext = (band_max[i], y_cord[i]), textcoords = 'data',\
            arrowprops=dict(edgecolor='black', arrowstyle = '|-|, widthA=0.3, widthB=0.3'))
        plt.text((band_max[i]+band_min[i]-35)/2, y_cord[i]+0.002, i+1, fontsize=8)

    plt.savefig(output+'Fig09_BandWavelengths.png')
    
#
# Query Satellite data, based on manual input location and time
#
def create_sat_arrays(dc, query, query2):
    sat_array = dc.load(product='ls8_nbar_scene', **query)
    sat_bigarray = dc.load(product='ls8_nbar_scene', **query2)
    sat_array.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'}, inplace=True)
    sat_bigarray.rename({'1': 'coastal_aerosol', '2': 'blue', '3': 'green', '4': 'red', '5': 'nir', '6': 'swir1', '7': 'swir2'}, inplace=True)
    return sat_array, sat_bigarray

#
# # Figure 10
#
### Plot relative locations of field and satellite data
#
def FIG_sat_field_locations(ground_brdf, sat_array, colpac, output, field_data):

    wgs_84 = pyproj.Proj(init='epsg:4326')
    aus_albers = pyproj.Proj(init='epsg:3577')

    xloc = [pyproj.transform(wgs_84, aus_albers, ground_brdf['Longitude'][i], ground_brdf['Latitude'][i]) for i in range(len(ground_brdf))]

    relxloc = [(xloc[i][0]-xloc[0][0], xloc[i][1]-xloc[0][1]) for i in range(len(ground_brdf))]

    satloc = [[0 for x in range(2)] for y in range(len(sat_array.x)*(len(sat_array.y)))]
    count=0
    for i in range(len(sat_array.x)):
        for j in range(len(sat_array.y)):
            satloc[count][0] = float(sat_array.x[i]-xloc[0][0])
            satloc[count][1] = float(sat_array.y[j]-xloc[0][1])
            count+=1

    satloc_df = pd.DataFrame(satloc)

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9.5, 9.5))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+': GeoLocations for data taken with LS8 (black) and field data (colours).\nReference position = '+str(xloc[0][0])+', '+str(xloc[0][1]), fontweight='bold')
    plt.tight_layout(pad=4.0, w_pad=1.0, h_pad=1.0)

    def gridlines(satloc_df):
        axes.axhline(satloc_df[1].unique()[0]+12.5, linestyle='--', color='black', linewidth=0.5)
        for i in range(len(satloc_df[1].unique())):
            axes.axhline(satloc_df[1].unique()[0]-(12.5+(25*i)), linestyle='--', color='black', linewidth=0.5)

        axes.axvline(satloc_df[0].unique()[0]-12.5, linestyle='--', color='black', linewidth=0.5)
        for i in range(len(satloc_df[0].unique())):
            axes.axvline(satloc_df[0].unique()[0]+(12.5+(25*i)), linestyle='--', color='black', linewidth=0.5)


    rr = pd.DataFrame(relxloc)

    ground_brdf_XY = pd.concat([ground_brdf, rr], axis=1)
    ground_brdf_XY.rename(columns={0: 'RelX', 1: 'RelY'}, inplace=True)

    for i in ground_brdf_XY.Line.unique():
        ground_brdf_XY[(ground_brdf_XY['Line']==i)].plot.scatter('RelX', 'RelY', ax=axes, color=colpac[i])

    satloc_df.plot.scatter(0,1, ax=axes, color='black', )

    axes.set_xlabel("Relative Aus Albers Longitude (m)")
    axes.set_ylabel("Relative Aus Albers Latitude (m)")

    gridlines(satloc_df)

    plt.savefig(output+'Fig10_SatFieldLocations.png')
    return xloc
    
#
# Create Australian Albers columns for ground_brdf (not used)
#
def create_albers_cols(ground_brdf):
    for i in range(len(ground_brdf)):
        ground_brdf['Xalbers'], ground_brdf['Yalbers'] = pyproj.transform(wgs_84, aus_albers, ground_brdf['Longitude'][i], ground_brdf['Latitude'][i])

    print(ground_brdf['Xalbers'][4], ground_brdf['Yalbers'][4])

    pyproj.transform(wgs_84, aus_albers, ground_brdf['Longitude'][4], ground_brdf['Latitude'][4])
    
#
# ### Create Field full band xarray
#
# The field xarray is based on the pixel locations of the satellite data, where
# each pixel contains an average of all field data measurements that fall
# within the pixel.
#
def create_field_from_sat(sat_array, ground_brdf, xloc):
    field_array = sat_array.astype(float)

    for i in range(len(sat_array.x)):
        for j in range(len(sat_array.y)):
            count = 0
            cum1, cum2, cum3, cum4, cum5, cum6, cum7 = 0,0,0,0,0,0,0
            for k in range(len(xloc)):
                if (sat_array.x[i]-12.5 < xloc[k][0] < sat_array.x[i]+12.5) and (sat_array.y[j]-12.5 < xloc[k][1] < sat_array.y[j]+12.5):
                    cum1 = cum1+ground_brdf.iloc[k]['band1']
                    cum2 = cum2+ground_brdf.iloc[k]['band2']
                    cum3 = cum3+ground_brdf.iloc[k]['band3']
                    cum4 = cum4+ground_brdf.iloc[k]['band4']
                    cum5 = cum5+ground_brdf.iloc[k]['band5']
                    cum6 = cum6+ground_brdf.iloc[k]['band6']
                    cum7 = cum7+ground_brdf.iloc[k]['band7']
                    count=count+1
            if count<10:
                field_array.coastal_aerosol[0][j][i] = np.nan
                field_array.blue[0][j][i] = np.nan
                field_array.green[0][j][i] = np.nan
                field_array.red[0][j][i] = np.nan
                field_array.nir[0][j][i] = np.nan
                field_array.swir1[0][j][i] = np.nan
                field_array.swir2[0][j][i] = np.nan
            else:
                field_array.coastal_aerosol[0][j][i] = cum1*10000/count            
                field_array.blue[0][j][i] = cum2*10000/count
                field_array.green[0][j][i] = cum3*10000/count
                field_array.red[0][j][i] = cum4*10000/count
                field_array.nir[0][j][i] = cum5*10000/count
                field_array.swir1[0][j][i] = cum6*10000/count
                field_array.swir2[0][j][i] = cum7*10000/count
    return field_array                

#
### FIGURE 11
#
# Plot large-area context RGB array for satellite data
#
def FIG_sat_bigRGB(sat_bigarray, output, field_data):
    DEAPlotting.three_band_image(sat_bigarray, bands = ['red', 'green', 'blue'], time = 0, contrast_enhance=False)
    plt.title(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' Large Area Context: RGB colours', fontweight='bold')

    plt.savefig(output+'Fig11_Satellite_bigRGB.png')

#
### FIGURE 12
#
# Plot RGB array for satellite data
#
def FIG_sat_RGB(sat_array, output, field_data):
    DEAPlotting.three_band_image(sat_array, bands = ['red', 'green', 'blue'], time = 0, contrast_enhance=False)

    plt.title(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+' RGB colours', fontweight='bold')
    plt.savefig(output+'Fig12_Satellite_RGB.png')
    
#
### FIGURE 13
#
# Plot RGB array for Field data
#
def FIG_field_RGB(field_array, output, field_data):
    DEAPlotting.three_band_image(field_array, bands = ['red', 'green', 'blue'], time = 0, contrast_enhance=False)

    plt.title(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+'Field RGB colours', fontweight='bold')
    plt.savefig(output+'Fig13_Field_rgb.png')
    
#
## Figure 14
#
### Plot ratio arrays for each band
#
# Each panel shows the ratio of satellite/field data.
#
def FIG_ratio_arrays(sat_array, field_array, output, field_data):
    newarr = sat_array/field_array
    newarr.reset_index('time', drop=True, inplace=True)

    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(11.5, 9.5))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+': Ratio of satellite/field reflectance', fontweight='bold')

    newarr.coastal_aerosol.plot(ax=axes[0,0])
    newarr.blue.plot(ax=axes[0,1])
    newarr.green.plot(ax=axes[0,2])
    newarr.red.plot(ax=axes[1,0])
    newarr.nir.plot(ax=axes[1,1])
    newarr.swir1.plot(ax=axes[1,2])
    newarr.swir2.plot(ax=axes[2,0])
    plt.tight_layout(pad=3.0, w_pad=1.0, h_pad=1.0)

    axes[2,1].axis('off')
    axes[2,2].axis('off')
    plt.savefig(output+'Fig14_RatioSatOverFieldData.png')
    
#
### Create statistics dataframe, comparing satellite and field data
#
def create_stats(sat_array, ground_brdf):
    data_array = np.array([['','LS8_mean','LS8_SD', 'Field_mean', 'Field_SD'],
                    ['Band1', float(sat_array.coastal_aerosol.mean()/10000), float(sat_array.coastal_aerosol.std()/10000), float(ground_brdf['band1'].mean()), float(ground_brdf['band1'].std())],
                    ['Band2', float(sat_array.blue.mean()/10000), float(sat_array.blue.std()/10000), float(ground_brdf['band2'].mean()), float(ground_brdf['band2'].std())],
                    ['Band3', float(sat_array.green.mean()/10000), float(sat_array.green.std()/10000), float(ground_brdf['band3'].mean()), float(ground_brdf['band3'].std())],
                    ['Band4', float(sat_array.red.mean()/10000), float(sat_array.red.std()/10000), float(ground_brdf['band4'].mean()), float(ground_brdf['band4'].std())],
                    ['Band5', float(sat_array.nir.mean()/10000), float(sat_array.nir.std()/10000), float(ground_brdf['band5'].mean()), float(ground_brdf['band5'].std())],
                    ['Band6', float(sat_array.swir1.mean()/10000), float(sat_array.swir1.std()/10000), float(ground_brdf['band6'].mean()), float(ground_brdf['band6'].std())],
                    ['Band7', float(sat_array.swir2.mean()/10000), float(sat_array.swir2.std()/10000), float(ground_brdf['band7'].mean()), float(ground_brdf['band7'].std())],
                    ])

    stat_df = pd.DataFrame(data=data_array[1:,1:],
                      index=data_array[1:,0],
                      columns=data_array[0,1:])

    stat_df['LS8_SD/mean (%)'] = 100*stat_df['LS8_SD'].astype(float)/stat_df['LS8_mean'].astype(float)
    stat_df['Field_SD/mean (%)'] = 100*stat_df['Field_SD'].astype(float)/stat_df['Field_mean'].astype(float)
    stat_df['LS8/Field'] = stat_df['LS8_mean'].astype(float)/stat_df['Field_mean'].astype(float) 

    fstat_df = stat_df.astype(float)
    return fstat_df

#
# # Figure 15
#
### Plot comparison spectra of ALL satellite and field data, on a
### pixel-by-pixel basis
#
# Error bars are shown for the field data, based on the standard deviation of
# the pixels within the field.
#
def FIG_ALL_sat_field_bands(fstat_df, output, field_data):
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9.5, 9.5))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+': Satellite and Field data comparison by band', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    fstat_df.plot(x=fstat_df.index, y='LS8_mean', ax=axes, color='black')
    fstat_df.plot(y='Field_mean', ax=axes, color='blue')
    axes.set_ylabel('Reflectance')
    plt.errorbar(x=fstat_df.index, y=fstat_df['Field_mean'], yerr=fstat_df['Field_SD'], color='blue')
    axes.set_xticklabels(['Band0','Band 1','Band 2','Band 3','Band 4','Band 5','Band 6', 'Band 7'])
    plt.savefig(output+'Fig15_LS8FieldBandCompare.png')
    
#
# Create a statistics dataframe to compare field and satellite for a subset of pixels
#
def create_SUB_stats(sat_array, field_array, fstat_df, inpix):

    inner_array = np.array([['', 'LS8_inner_mean', 'Field_inner_mean'],
                            ['Band1', float(sat_array.coastal_aerosol[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.coastal_aerosol[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band2', float(sat_array.blue[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.blue[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band3', float(sat_array.green[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.green[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band4', float(sat_array.red[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.red[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band5', float(sat_array.nir[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.nir[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band6', float(sat_array.swir1[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.swir1[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                            ['Band7', float(sat_array.swir2[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000), float(field_array.swir2[0][inpix[0]:inpix[1],inpix[2]:inpix[3]].mean()/10000)],
                           ])

    inner_df = pd.DataFrame(data=inner_array[1:,1:],
                      index=inner_array[1:,0],
                      columns=inner_array[0,1:])

    inner_df['Field_SD'] = fstat_df['Field_SD']

    finner_df = inner_df.astype(float)
    return finner_df

#
## Figure 16
#
### Plot comparison spectra of INNER satellite and field data, on a
### pixel-by-pixel basis
#
# Error bars are shown for the field data, based on the standard deviation of
# the pixels within the field.
#
# Only inner pixels are chosen to compare, where there are many field spectra
# for each satellite pixel. For example, using [2:4,2:4] will choose four
# pixels between coordinates (2,2) and (3,3), inclusive, from the top-left
# corner.
#
def FIG_SUB_sat_field_bands(finner_df, output, field_data):
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9.5, 9.5))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+': Satellite and Field data comparison by band for inner pixels', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    finner_df.plot(x=finner_df.index, y='LS8_inner_mean', ax=axes, color='black')
    finner_df.plot(y='Field_inner_mean', ax=axes, color='blue')
    axes.set_ylabel('Reflectance')
    plt.errorbar(x=finner_df.index, y=finner_df['Field_inner_mean'], yerr=finner_df['Field_SD'], color='blue')
    axes.set_xticklabels(['Band0','Band 1','Band 2','Band 3','Band 4','Band 5','Band 6', 'Band 7'])
    plt.savefig(output+'Fig16_InnerLS8FieldBandCompare.png')
    
#
# # Figure 17
#
### Comparison plot of Field and satellite data
#
# Plot shows a pixel-by-pixel comparison of all pixels where field data exists.
# Different band data are shown in different colours and different symbols.
#
def FIG_sat_field_scatter_compare(sat_array, field_array, output, field_data):
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(9.5, 9.5))
    fig.suptitle(field_data[3]+': '+field_data[0]+' '+field_data[1]+' '+field_data[2]+': Pixel by pixel comparison of field and satellite data', fontweight='bold')
    plt.tight_layout(pad=3.5, w_pad=1.0, h_pad=1.0)

    plot_scale = [0.0, 0.3, 0.0, 0.3]
    plt.xlim(plot_scale[0], plot_scale[1])
    plt.ylim(plot_scale[2], plot_scale[3])
    p1, p2 = [-1, 2], [-1, 2]
    plt.plot(p1, p2, marker='o')
    plt.xlabel('Field Reflectance per pixel')
    plt.ylabel('Satellite Reflectance per pixel')

    plt.scatter(field_array.coastal_aerosol[0]/10000, sat_array.coastal_aerosol[0]/10000, marker='o', facecolors='none', edgecolors='red')
    plt.scatter(field_array.blue[0]/10000, sat_array.blue[0]/10000, marker='^', facecolors='none', edgecolors='orange')
    plt.scatter(field_array.green[0]/10000, sat_array.green[0]/10000, marker='s', facecolors='none', edgecolors='yellow')
    plt.scatter(field_array.red[0]/10000, sat_array.red[0]/10000, marker='+', color='green')
    plt.scatter(field_array.nir[0]/10000, sat_array.nir[0]/10000, marker='x', color='blue')
    plt.scatter(field_array.swir1[0]/10000, sat_array.swir1[0]/10000, marker='D', facecolors='none', edgecolors='darkblue')
    plt.scatter(field_array.swir2[0]/10000, sat_array.swir2[0]/10000, marker='*', facecolors='none', edgecolors='black')

    x_stretch = (plot_scale[1]-plot_scale[0])
    y_stretch = (plot_scale[3]-plot_scale[2])

    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.950*y_stretch)+plot_scale[2], marker='o', facecolors='none', edgecolors='red')
    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.925*y_stretch)+plot_scale[2], marker='^', facecolors='none', edgecolors='orange')
    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.900*y_stretch)+plot_scale[2], marker='s', facecolors='none', edgecolors='yellow')
    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.875*y_stretch)+plot_scale[2], marker='+', color='green')
    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.850*y_stretch)+plot_scale[2], marker='x', color='blue')
    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.825*y_stretch)+plot_scale[2], marker='D', facecolors='none', edgecolors='darkblue')
    plt.scatter((0.1*x_stretch)+plot_scale[0], (0.800*y_stretch)+plot_scale[2], marker='*', facecolors='none', edgecolors='black')

    plt.figtext(0.185, 0.895, "Band 1 - Coastal Aerosol")
    plt.figtext(0.185, 0.872, "Band 2 - Blue")
    plt.figtext(0.185, 0.850, "Band 3 - Green")
    plt.figtext(0.185, 0.830, "Band 4 - Red")
    plt.figtext(0.185, 0.809, "Band 5 - NIR")
    plt.figtext(0.185, 0.786, "Band 6 - SWIR1")
    plt.figtext(0.185, 0.766, "Band 7 - SWIR2")
    plt.savefig(output+'Fig17_PixelByPixelComparison.png')


