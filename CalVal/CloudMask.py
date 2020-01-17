import pandas as pd
import numpy as np


###############################################################################
# Flatten lists that have extraneous dimensions                               #
###############################################################################
def flatten(foo):
    for x in foo:
        if hasattr(x, '__iter__') and not isinstance(x, str):
            for y in flatten(x):
                yield y
        else:
            yield x

###############################################################################
# Make an array that is ready to be checked for cloud and cloud shadow. Steps #
# involved here include:                                                      #
#                                                                             #
#   1. Flag out bad data                                                      #
#   2. Smooth data in x and y to reduce effects of small ground variations    #
#      and enhance effects of large clouds spread over areas > 500m.          #
#   3. Drop long wavelength data and focus on CA, BGR data.                   #
#   4. Create median of all remaining data.                                   #
#   5. Based on median, create difference data that will highlight temporal   #
#      changes - ie. cloud and shadow.                                        #
#   6. Average remaining four bands together to give greatest contrast.       #
###############################################################################
def make_processed_array(ls8_bigarray, satname):

    # Test to see which satellite we are using and then set the appropriate
    # pixel scale.
    if satname == "LS8":
        pixscale = 25
    else:
        pixscale = 10

    # Remove flagged out data with values of -999
    unflagged_array = ls8_bigarray.where(ls8_bigarray > 0)

    # Smooth data in x and y by 500/pixscale pixels (ie. 20 pix for LS8 and 50
    # pix for Sentinel 2) and drop any NaNs which will be at the edges of the 
    # images.
    smooth_array_x = unflagged_array.rolling(x=int(500/pixscale)).mean().dropna('x')
    smooth_array_xy = smooth_array_x.rolling(y=int(500/pixscale)).mean().dropna('y')

    # Drop long wavelength data to focus on Coastal Aerosol, plus RGB for
    # cloud masking.
    if satname == "LS8":
        ls8_cbgr_array = smooth_array_xy.drop(['nir', 'swir1', 'swir2'])
    else:
        ls8_cbgr_array = smooth_array_xy.drop(['nbart_red_edge_1',
                                        'nbart_red_edge_2', 'nbart_red_edge_3',
                                        'nbart_nir_1', 'nbart_nir_2', 
                                        'nbart_swir_2', 'nbart_swir_3'])

    # Create median of all data, crunching along the time axis.
    ls8_median = ls8_cbgr_array.median(dim='time')

    # Make an array that is the difference of the original data, compared to
    # the median image.
    ls8_diff = ls8_cbgr_array - ls8_median

    # Average over the four bands
    if satname == "LS8":
        ls8_avg = (ls8_diff.coastal_aerosol+ls8_diff.blue+ls8_diff.green+ls8_diff.red)/4
    else:
        ls8_avg = (ls8_diff.nbart_coastal_aerosol+ls8_diff.nbart_blue+ls8_diff.nbart_green+ls8_diff.nbart_red)/4

    return ls8_avg

###############################################################################
# Threshold mask data to identify dates with significant cloud or shadow      #    
###############################################################################
def threshold_mask(ls8_avg):

    # COARSE THRESHOLDING. This step is used to remove the worst of the cloud-
    # affected data only.
    #
    # Identify dates where mean < 1000 and standard deviation < 200. These are
    # the data with good dates (threshold1).
    threshold1 = ls8_avg.where(abs(ls8_avg.mean(dim=('y','x'))) < 1000)
    threshold1 = threshold1.where(threshold1.std(dim=('x','y')) < 200)
    threshold1 = threshold1.dropna('time')
    
    # Based on the good dates so far, create an xarray with just the bad dates
    # (threshold1bad)
    threshold1bad = ls8_avg.copy()
    
    for i in threshold1.time:
        threshold1bad = threshold1bad.drop(i.values, dim='time')
    
    # Based on just the good dates from coarse thresholding (threshold1),
    # create a median image and then subtract that median from each remaining
    # good date (ls8_median2) to create a new xarray with difference data
    # (threshold2).    
    ls8_median2 = threshold1.median(dim='time')
    
    threshold2 = threshold1 - ls8_median2
    
    # FINE THRESHOLDING. This step removes remaining cloud-affected data.
    #
    # Retain only dates where -600 < mean < 750 and
    # -700 < maximum pixel value < 700
    # This creates an xarray of good data (threshold3).
    threshold3 = threshold2.copy()
    threshold3 = threshold3.where(np.logical_and(threshold3.mean(dim=('y','x')) < 750,
                                       threshold3.mean(dim=('y','x')) > -600))
    threshold3 = threshold3.where(threshold3.max(dim=('y','x')) < 700)
    threshold3 = threshold3.where(threshold3.min(dim=('y','x')) > -700)
    
    threshold3 = threshold3.dropna('time')
    
    # Create a bad date xarray (threshold3bad), based on the full dataset
    # (threshold1) which includes all the bad dates for the fine thresholding
    # step only.
    threshold3bad = threshold1.copy()
    
    for i in threshold3.time:
        threshold3bad = threshold3bad.drop(i.values, dim='time')

    # Create a list (daylist) that contains all the dates that have been
    # flagged out as bad. Return this list.
    # Also, print out the number of dates that were captured in both the
    # coarse and fine thresholding steps.
    daylist = []
    for i in threshold1bad.time.values:
        daylist.append(str(i)[0:10])
    print("Coarse threshold finds this many bad days:", len(threshold1bad.time))
    for i in threshold3bad.time.values:
        daylist.append(str(i)[0:10])
    print("Fine threshold finds this many bad days:", len(threshold3bad.time))
    
    return daylist

###############################################################################
# Print out differences between the auto and manual masking methods.          #    
#                                                                             #    
# Note that the manual masking method is to visually identify each date that  #    
# contains bad data due to cloud or shadow and create the ls8_bad_days list.  #    
# The auto masking method is the thresholding method contained within this    #    
# file.                                                                       #    
###############################################################################
def report_differences(ls8_bad_days, daylist):
    ManualVAuto = list(set(ls8_bad_days) - set(daylist))
    AutoVManual = list(set(daylist) - set(ls8_bad_days))
    ManualVAuto.sort()
    AutoVManual.sort()
    print("Number of days in manual cloud mask, but not in auto cloud mask (ie. Auto did not mask enough?):", len(ManualVAuto), "\n"
          "Number of days in auto cloud mask, but not in manual cloud mask (ie. Auto masked too much?):", len(AutoVManual), "\n\n")
          # Uncomment following two lines and remove ")" from above line to see
          # the dates that are different between manual and auto masking.
          #"Manual cloud mask days missed in auto mask:", ManualVAuto, 
          #"\n\nAuto cloud mask days missed in manual mask:", AutoVManual)

###############################################################################
# Combine previous functions to run entire cloud mask and return "daylist",   #
# which contains all the cloud-affected days.                                 #
###############################################################################
def cloud_mask(ls8_bigarray, ls8_bad_days, satname):
    ls8_avg = make_processed_array(ls8_bigarray, satname)
    daylist = threshold_mask(ls8_avg)
    report_differences(ls8_bad_days, daylist)

    return daylist
