<H1>Instructions for processing MultiTimeLine workflow</H1>

This workflow follows on from the Site-Pipelines workflow. It produces a
time-series for the field site of both Landsat and Sentinel data, since the
beginning of 2013. The first part of the workflow is the same as the
Site-Pipelines workflow, so if Site-Pipelines has successfully completed, then
this workflow should require some minor* tweaking.<P>

Within the MultiTimeLine directory, there will be a template.ipynb file,
which can be used as a starting point. Copy this file and edit the first cell
as for the Site-Pipelines workflow. There are a few extra fields that need to
be filled in here:
<OL>
    <LI><B>ls8_bad_days, s2a_bad_days, s2b_bad_days</B>. These lists contain
        the dates for which the satellite data shows cloud and are therefore
        flagged out. Initially these lists should be left blank.</LI>
    <LI><B>ls8_csvs, sent_csvs</B>. These lists contain the name of a CSV file
        that was created in the penultimate cell of the Site-Pipelines workflow.
        The CSV file contains an output of the summary fstat_df DataFrame and
        the summary field data contained within is used to plot against the
        satellite data. In order to generate data points for both Landsat and
        Sentinel, The corresponding Site-Pipelines workflow needs to be run
        twice: once with field_data[3] set to "Landsat8" and once with
        field_data[3] set to "Sentinel2a" or "Sentinel2b".</LI>
    <LI><B>rain_dat</B>. The string points to a CSV file in the Weather
        subdirectory, which contains historical rainfall data close to the field
        site. The data must be manually generated from the BOM website, as
        described below.</LI>
</OL>

### Generating rainfall CSV data

In this example, Blanchetown rainfall data is generated. The first step is to
download the closest rain gauge data over the time period 2013-present:
<OL>
    <LI>Go to the <A HREF=http://www.bom.gov.au/climate/data/index.shtml>BOM
        Climate Data Online</A> website.</LI>
    <LI>Above the map, click the tab "Select using text".</LI>
    <LI>Under point 2 "Select a weather station in the area of interest", enter
        the name of the place you are looking for and click "Find". If you
        do not know the name, it is also possible to search by position, using
        the button on the far right-hand-side.</LI>
    <LI>You will be presented with a list of matching towns. Click on the most
        appropriate one.</LI>
    <LI>You will be presented with a list of the nearest rainfall gauges. Click
        on the closest one. Below this, a small graph will show you the date
        range over which this station has been collecting rainfall data. If the
        station has not been collecting enough data in the period since 2013,
        you may need to pick another station.</LI>
    <LI>Once you have chosen the appropriate station, click on the "Get Data"
        button under step 3 (at the bottom of the page). This will take you to
        a daily rainfall spreadsheet for the current year.</LI>
    <LI>You can download all the rainfall data (all years) for the station by
        clicking on the link "All years of data", found in the top-right corner
        of the page. This will initiate downloading of a zip file, which, when
        expanded, contains a CSV file with all the relevant rainfall data.</LI>
</OL>
Once you have the CSV of the rainfall data, you should move it to a CSV
directory in the top level. For example, if you have the CSV file in the
MultiTimeLine directory, and you are in that directory:

    > mv IDCJAC0009_024564_1800_Data.csv ../CSV/

Note, you may need to first create the CSV directory ("mkdir ../CSV").
<BR><BR><BR>* Easy, but laborious.
