import pandas as pd
import numpy as np
import os
import math
from datetime import date


###############################################################################
# Use shell script to access BOM web interface. First extract the relevant    #
# relevant webpage that has the link to the full rain data, then retrieve     #
# rain data zip file, unzip and return csv file.                              #
###############################################################################
def retrieve_rain_gauge_data(ID):
    # Create shell script
    file = open('tempfile.txt', 'w')
    file.write('aaa=$(wget "http://www.bom.gov.au/jsp/ncc/cdio/weatherData/av?p_nccObsCode=136&p_display_type=dailyDataFile&p_startYear=&p_c=&p_stn_num='+format(ID, '06d')+'" -O log ; grep "All years" log | awk \'{print $25}\' - | cut -c7-151 - | sed "s/amp;//g" -)\nrm -f log\nbbb=$(echo -n "http://www.bom.gov.au"$aaa)\nwget $bbb -O temp.zip\nunzip temp.zip -x *Note*\nrm -f temp.zip\n')
    file.close()
    
    os.system('chmod u+x tempfile.txt')
    os.system('./tempfile.txt')
    os.system('rm -f tempfile.txt')
    os.system('pwd')
    
    csvfile = str('IDCJAC0009_'+format(ID, '06d')+'_1800_Data.csv')
    return pd.read_csv(csvfile)

###############################################################################
# This script will take a set of Latitude, Longitude coordinates and identify #
# the nearest rain gauge to the site that is operational in the window of     #
# 2013-2019. It will then download the rain data from the BOM website and put #
# it in the calval/Weather directory to be used with the MultiTimeLine        #
# workflow.                                                                   #
###############################################################################

def get_rain_data(lat, lon):

    #
    # Read into a Pandas DF the full list of rain gauge stations.
    # This file contains station ID, lattitude, longitude and name.
    #
    df = pd.read_csv('/g/data/u46/users/aw3463/GuyByrne/calval/Weather/ShortStations.txt')
    
    # Read in coordinates to search around
    data2 = {'Lat': pd.Series(lat),
             'Lon': pd.Series(lon)}
    
    #
    # Copy into DataFrames.
    # df1 = full list of rain gauge stations
    # df2 = location for this field site
    #
    df1 = df.copy()
    df2 = pd.DataFrame(data2)

    #
    # Calculate distances for all rain gauges from point of interest
    # Distances are in approximate kilometres, assuming that 1 degree of
    # latitude = 111.6km.
    #
    df1['dist'] = [111.6*math.sqrt((math.cos(math.radians(df2.Lon[0]))*(df1.Lon[i]-df2.Lon[0]))**2 + (df1.Lat[i]-df2.Lat[0])**2) for i in range(len(df1))]

    #
    # Loop through the rain gauges, starting with the nearest
    #
    for i in range(len(df1.index)):
        ID = df1.sort_values('dist')[:i+1].ID.values[i]
        
        # Retrieve rain gauge CSV file from BoM website
        rain_gauge = retrieve_rain_gauge_data(ID)

        # Calculate how many days there are between the start of 2013 and today
        DaysSince2013 = (date.today() - date(2013, 1, 1)).days   

        # Test to see if there are at least 95% of days between 2013 and today
        # that have real rain measurements (not NaNs when the rain gauge was
        # not operational
        if float(rain_gauge[rain_gauge.Year >= 2013]['Rainfall amount (millimetres)'].count())/float(DaysSince2013) > 0.95:
            # If the rain gauge has good data (>95%), then move the CSV file
            # into a permanent location and break out of the loop, as we have
            # found the nearest rain gauge with good data.
            os.system('mv -f IDCJAC0009_'+format(ID, '06d')+'_1800_Data.csv /g/data/u46/users/aw3463/GuyByrne/calval/Weather')
            break

    # Print out the details of the rain gauge, including distance from field
    # site in km.
    print('Nearest Rain Gauge Station - ', "%.2f" % df1[df1.ID==ID]['dist'].values[0], 'km away')
    print('\n-------------------------------------------\n')
    print(df[df.ID==ID])

    # Return the string that contains the relative location and name of the
    # rain gauge CSV file data.
    return '../Weather/IDCJAC0009_'+format(ID, '06d')+'_1800_Data.csv'
