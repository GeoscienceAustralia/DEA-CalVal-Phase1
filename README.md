# README #

This repository contains workflow files for the comparison of field and
satellite data for calibration/validation. This includes python code, as well
as jupyter notebooks. The structure looks like:

<B>CalVal</B> - Python code for the workflows.<BR>
<B>MultiTimeLine</B> - Jupyter notebook workflows for creating site timelines
since 2013.<BR>
<B>Site-Pipelines</B> - Jupyter notebook workflows for comparing field and
satellite data.<BR>
<B>Weather</B> - CSV files for nearest rain gauges, with day zero set to
31/12/2017.<BR>
<B>brdf</B> - files for creating BRDF corrections required by workflows.<BR>
<B>Misc</B> - Miscellaneous files, including Panel calibration spectra,
Satellite band response files etc.<BR>
<B>README.md</B> - This Readme file.<P>

<HR>
  
<H2>Instructions for processing Site-Pipelines workflow</H2> 

These instructions are designed to be a step-by-step walk-through of the
workflow to process field data and compare them to satellite data, or a new
field dataset. It is assumed that this workflow will be run on the NCI's VDI
platform, as the Digital Earth Australia (DEA) module is required to run the
workflows.<P>

### Pre-requisites

In order for the workflow to run, there are a number of other assumed
requirements that should be met. Go through this check-list before running
the workflow for the first time:
<OL>
<LI>The Python library for this workflow can be found on VDI and should be
downloaded from this repo (<B>CalVal</B> directory) or copied into the working
directory directly on VDI:<BR><BR>
    cp -r /g/data/u46/users/aw3463/GuyByrne/calval/CalVal .<BR><BR>
<LI>The DEAPlotting library is also needed for RGB plots and can be obtained
from https://github.com/GeoscienceAustralia/dea-notebooks under "10_Scripts" or can be copied on VDI to the working directory:<BR><BR>
    cp /g/data/u46/users/aw3463/GuyByrne/calval/DEAPlotting.py .<BR><BR>
<LI>Start up the DEA module by typing:<BR><BR>
    > module load dea<BR><BR>
<LI>Copy the template in the Site-Pipelines directory to a new file and then
start the notebook. eg:<BR><BR>
    > cp template.ipynb Pipeline-LG-26-03-18.ipynb<BR>
    > jupyter notebook Pipeline-LG-26-03-18.ipynb<BR><BR>
<LI>Input and output directories should be defined in the first cell, as
'indir' and 'output', respectively. For the input directory, it is assumed
that there are multiple sub-directories, with format 'line1, line2, line3' etc.
Note that lower case is required and no extra characters are allowed in the
directory names. So 'Line1' or 'line_1' will not work. The output directory
will be created by the workflow and is where PNG files will be stored, as well
as the data sheet text file.<BR>
<B>NOTE:</B> Each time the workflow is run, the output directory will be erased
and re-written, so that the directory can be cleaned up. If you want to save
older PNGs, you need to manually move them before re-running the
notebook.<BR><BR>
<LI>Within each 'line' sub-directory, there should be radiance spectrum files
in text format, with extension '.asd.rad.txt'.<BR><BR>
<LI>There are standard files that are used for determining the panel K-factor,
currently located either in this repo under <B>Misc</B> or:<BR><BR>
        /g/data/u46/users/aw3463/GuyByrne/30APR18/Panels/<BR><BR>
<LI>Satellite band response files are located either in this repo under
<B>Misc</B> or in the directory:<BR><BR>
        /g/data1a/u46/users/aw3463/GuyByrne/misc_others/<BR><BR>
        including landsat8_vsir.flt, Sent2a.flt and Sent2b.flt.<BR><BR>
<LI>The 'field_data' list should be edited to contain the relevant information
on: <BR>
1. Three-letter field name (eg. LKG for Lake George)
2. Date of field site measurement (format: DDMMMYY)
3. Extra field site information (eg. Site1/2 or CSIRO)
4. Satellite name (must be one of Landsat8, Sentinel2a, Sentinel2b)
5. The name of the panel K-factor to use
6. Whether the data were recorded in Radiance or Reflectance mode.

<LI>The lists 'bad_pans' and 'bad_grounds' can be left as empty for the first
time running the workflow (eg. 'bad_pans = []'). These are used to specify
any bad panel or ground readings identified later on.<BR><BR>
<LI>Variables firstGoodLine, firstGroundSpec and firstGoodPanelSpec need to be
specified. These are determined from knowledge of the field data and can be
used to eliminate bad data at the start of the field collection. If all goes
well, normally the first good line is number 1, the first good panel is number
0 and the first good ground spectrum is number 2. ie. there are two panel
spectra at the start of line 1 (spec=0 and 1), followed by the first ground
(spec=2).<BR><BR>
<LI>The BRDF correction requires a separate directory and a new window on VDI.
Do NOT use a window where you have already typed 'module load dea' because it
needs slightly different modules. In this example, the directory
'/g/data/u46/users/aw3463/GuyByrne/calval/brdf' is used (a copy is also in this
repo under the <B>brdf</B> directory). Once you have created your own directory
and you have changed into that directory, type the following to copy over the
required files:<BR><BR>
        > cp /g/data/u46/users/aw3463/GuyByrne/calval/brdf/* .<BR><BR>
</OL>

### Calculating BRDF correction

One of the first things you need to do in this notebook is calculate the BRDF
correction, but this requires that you read in the field data so that the
latitude, longitude and time of the field data can be used to create the
correction. Do the following steps:

<OL>
<LI>Run the first five cells of the workflow.
<LI>The fifth cell will print out scripts for determining the BRDF correction.
You will see the script output below something like:<BR><BR>
        
        
        ###################################################################<BR>
        # Copy and paste the following into a terminal window on VDI for
SATELLITE data  #<BR>
        ###################################################################<BR><BR>
        
        
where 'SATELLITE' is either 'Landsat 8' or 'Sentinel 2'.<BR><BR>
<LI>Copy and paste the output text directly into the brdf terminal
window.<BR><BR>
<LI>The result in the terminal window (takes about 30 seconds) will be a
formatted version of the 'brdf_data' numpy array. This can be directly copied
and pasted over the top of the existing brdf_data array at the bottom of the
first cell in the notebook.<BR><BR>
</OL>

### Running the notebook
Once the BRDF correction has been added to the notebook, it should be possible to run the notebook in its entirety. To do this, go to the top of the Jupyter Notebook and click on 'Kernel', then 'Restart & Run All', then click on the red button to confirm and run the workflow. It should take about 2-5 minutes to complete.

### Interpreting results of the first notebook run
Here, it is assumed that the notebook ran to completion, such that all the cells were processed. If the notebook stopped midway, then please see the <B>Troubleshooting</B> section below for some hints on what might have gone wrong.<BR><BR>
    
<B>Cell [4]</B> (Define 'alldata'...) lists a small section of the field data as a pandas dataframe. Only data for a wavelength of 350nm is shown. Check that the values in each column appear reasonable.<BR><BR>
    
<B>Figure 1</B> (Plot panel radiances...) will show overlay plots of panel radiances on both the left- and right-hand-sides, with the middle pane empty. All panel radiances should appear close together. If you notice a small number of panels that look significantly different, then these are probably bad panel radiances. You should try to identify the corresponding spectra and then add them to the 'bad_pans' list in Cell [2]. Once you have flagged the bad panel spectra, you should be able to re-run the notebook and this Figure will now show you the good and bad panels separated into the left and middle panes, respectively, with all panels together shown in the right pane.<BR><BR>
    
<B>Figure 2</B> (Diagnosis plots...) Will show various plots of any identified bad panel spectra. This is only used if you are curious about why some panel spectra may be misbehaving.<BR><BR>
    
<B>Figure 3</B> (Plot ground spectra...) shows two panes, which initially will be the same, showing an overlay of all the ground radiances (without panels). This plot can be used to identify any outlying ground radiances, which can be subsequently identified using 'bad_grounds' in Cell [2]. Once such bad radiances have been flagged, then the two panes will show a with/without comparison.<BR><BR>
    
<B>Figures 4 and 5</B> (Plot timelines...) will initially be the same. They show a line-by-line plot of the timelines of spectra taken, with the horizontal axis being seconds since the first spectrum was taken. Panel radiances are shown as blue crosses and ground radiances are shown as orange vertical lines. If there are any errant panel or graound radiances, based on the time they were taken, they can be identified here. Also, these plots can be used to assess when the panel readings for each line occur. If there are any bad panels or ground radiances, then they will be removed from the second figure.<BR><BR>
    
<B>Figure 6</B> (Create timeline...) Shows two panes with averaged radiances for panel spectra, as a function of time (in seconds, since the first spectrum). Initially they will show the same. The average panel readings should show a slowly changing curve that follows insolation. For example, field data taken in the morning will show a slowly rising curve, as the Sun rises. Deviatinos from this slowly changing curve may identify bad panel readings that should be flagged out in 'bad_pans' in Cell [2]. Once the notebook is re-run, any bad panels will be removed from the second pane.<BR><BR>
    
<B>Figure 7</B> (Plot all ground...) shows reflectance spectra for all good ground observations as black curves. Coloured curves show the average for all spectra in a Line. the right pane just shows a zoomed y-axis, compared to the left pane. Any unusually different spectra can be identified here and may be flagged in 'bad_grounds' in Cell [2].<BR><BR>
    
<B>Figure 8</B> (Plot band reflectances) shows the reflectance spectra convolved to the satellite bands.<BR><BR>
    
<B>Figure 9</B> (Histogram of all...) shows band-by-band histograms for all reflectances. The histograms typically conform to a Normal distribution, but unusually bright or dark spectra may be identified here.<BR><BR>
    
<B>Figure 10</B> (Plot satellite band...) show the median ground reflectance, together with the wavelength ranges for the satellite corresponding to the data. This is just to check that the satellite bands fall within well-behaved parts of the spectrum.<BR><BR>
    
<B>Figure 11</B> (Plot relative locations...) shows a relative longitude/latitude positions for both field and satellite data. A grid is also shown to represent the extent of the satellite pixels.<BR><BR>
    
<B>Figures 12, 13 and 14</B> show RGB images of the Satellite and field data, where the field data have been averaged into pixels that match the satellite data. Blank field pixels means that there is no field data corresponding to that pixel.<BR><BR>

<B>Figure 15</B> shows the band-by-band satellite data, together with representative variability values in the title. Variability is defined as the ratio of the standard deviation (or rms), divided by the mean for each band. This gives an indication of how much change there is across the field site. There should typically be less than 5% variability.<BR><BR>
    
<B>Figure 16</B> (Plot ratio arrays) shows band-by-band images of the ratio between satellite and field arrays. All images have been scaled to ratios between 0.9 and 1.1, such that green colours indicate a close match between field and satellite pixels.<BR><BR>
    
<B>Figure 17</B> (Plot comparison spectra...) shows a band-by-band comparison of satellite and field data. Three spectra are shown. Black is the average spectrum for <I>all</I> satellite pixels, orange is the average for only those satellite pixels that overlap with at least one field spectrum. The blue spectrum shows the average for all field data. Any difference between the orange and black spectra is indicative of the variation in the ground spectrum, as measured by the satellite at slightly varying positions, so it gives a guide for how reliable the satellite data is.<BR><BR>
    
<B>Figure 18</B> (Comparison plot of...) shows a scatter plot, comparing the satellite and field data where there is at least one field spectrum overlapping with each satellite pixel. Different bands are shown with different symbols and colours.<BR><BR>
    
<B>Figure 19</B> shows the same as Figure 17, but for each band all the pixel data is averaged, so there is one data point per band. Error-bars are shown, which represent the standard deviation of the satellite and field data.<BR><BR>
    
<B>Data Sheet</B> text file is written out to the PNG directory, which has some summary information on the
field site and corresponding satellite data.<BR><BR>
    
### Troubleshooting
If the notebook does not complete, there are a few likely causes that can be checked.<BR>
    
It is possible that field data were recorded without GPS location information in the header. In such cases, the header will appear like:

```
GPS-Latitude is S0
GPS-Longitude is E0
```

The notebook will automatically identify such cases and try to deal with them, but it needs to know the coordinates for the box over which the field data was measured. These coordinates are fed into the variable "Corners" at the bottom of Cell [3], along with a True/False declaration for "RockWalk". If no coordinates are given and datacube manages to find satellite data, datacube will try and find a map at (0,0) and fail.<BR><BR>

The 
