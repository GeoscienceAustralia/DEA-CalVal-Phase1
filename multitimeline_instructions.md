<H1>Instructions for processing MultiTimeLine workflow</H1>

This workflow follows on from the Site-Pipelines workflow. It produces a
time-series for the field site of both Landsat and Sentinel data, since the
beginning of 2013.

Multi Timelines requires code that sits in the SRC/Multi_TimeLine
subdirectory, as well as some code from the main SRC/Site_Pipelines
subdirectory.

Within the MultiTimeLine directory, there will be a template.ipynb file,
which can be used as a starting point. Copy this file and edit the first cell
as for the Site-Pipelines workflow. There are a few extra fields that need to
be filled in here:
<OL>
    <LI>The <B>Corners</B> list needs to be filled out with at least two
        coordinates (lat and long) for the site in question.</LI>
    <LI><B>ls8_csvs, sent_csvs</B>. These lists contain the name of a CSV file
        that was created in the penultimate cell of the Site-Pipelines workflow.
        The CSV file contains an output of the summary fstat_df DataFrame and
        the summary field data contained within is used to plot against the
        satellite data. In order to generate data points for both Landsat and
        Sentinel. The corresponding Site-Pipelines workflow needs to be run
        twice: once with field_data[3] set to "Landsat8" and once with
        field_data[3] set to "Sentinel2a" or "Sentinel2b". It is not necessary
        for csv files to be elements of these lists - they can be empty - but
        they must exist, even if empty.</LI>
</OL>

### Generating rainfall CSV data

Rainfall data is now automatically generated in Cell [3]. This Cell goes to the
BoM website and searches for a list of rain gauges that are closest to the
coordinates provided in the <B>Corners</B> list. The rainfall data are then
checked to make sure there are good data for at least 95% of the time, since the
beginning of 2013. If not, the next-closest rain gauge is checked, and so on.
When a suitable rain gauge is found, the rainfall data are downloaded into the
Weather directory. <B>rain_dat</B> points to the file in this directory.

### Cloud masking
There are automatic cloud mitigation strategies available for both Landsat and
Sentinel products, but in practice those built into DEA products do not result
in a satisfactory dataset, as too many good dates are flagged out and too many
bad dates remain in the final product. Instead, a cloud masking method was
developed just for this workflow.<P>

The steps to flag out cloud and cloud shadow can be summarised as:
<OL>
    <LI>Smooth data to an effective resolution fo 500m. This smooths out sharp
        lines from roads/buildings etc, as well as enhancing cloud effects,
        which are typically large-scale.</LI>
    <LI>Focus on just coastal aerosol, blue, green and red bands.</LI>
    <LI>Create a median of all data, over all time.</LI>
    <LI>Create dataset that is difference of CA/BGR data from median and search
        for large differences.</LI>
    <LI>Coarse thresholding: remove any data where difference is > 0.1 surface
        reflectance (SR) units, or where the standard deviation is larger than
        0.025 SR units.</LI>
    <LI>Based on remaining data, create new median and difference
        datasets.</LI>
    <LI>Fine thresholding: remove any data where the average SR of the field
        site is between -0.06 and 0.07. Also remove any data where any
        individual pixel within a field site shows a difference of more than
        0.07 SR units.</LI>
</OL>

Whilst this method improves upon the DEA standard method, there are still times
where good data may be flagged out, or bad data are kept in. Typically this may
happen once or twice per Multi-Timeline workflow.

### After the first run.

Once the notebook has run all the way through, you will now be able to see
satellite maps for each individual overpass.

Note that all the data
(including contaminated days) will still be shown in Cells [7-9]. However,
Cell [12] will show the summary spectra for only good satellite data. If you
see suspiciously different spectra here, it might mean you have not flagged out
all the bad data. Also Cell [13] (MultiTimeLine plots) will help any
contaminated data to stand out.
