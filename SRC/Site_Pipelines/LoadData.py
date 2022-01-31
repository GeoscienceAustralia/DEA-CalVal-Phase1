import datetime
import pandas as pd
import numpy as np
import glob, os, subprocess
import array
from . import ASD_reader



###############################################################################
#                                                                             #
# Action functions are defined to retrieve specific parts of the header for   #
# each spectrum. These functions are used in extract_metadata.                #
#                                                                             #
###############################################################################

# Instrument Number
def action1(l, Corners):
    return l[27:34]

# Datetime of spectrum
def action2(l, Corners):
    return l[16:38]

# SWIR1 gain
def action3(l, Corners):
    return l[15:33]

# SWIR2 gain
def action4(l, Corners):
    return l[15:33]

# GPS Latitude in decimal degrees
def action5(l, Corners):
    if 'GPS-Latitude is S0' in l:
        return Corners[0]
    else:
        return float(l[17:20])-float(l[20:27])/60

# GPS Longitude in decimal degrees
def action6(l, Corners):
    if 'GPS-Longitude is E0' in l:
        return Corners[1]
    else:
        return float(l[19:22])+float(l[22:30])/60

# GPS UTC for accurate timestamp (04MAR21 onwards)
def action7(l, Corners):
    return l[11:19]

################################################################################
#                                                                              #
# Based on action functions defined above, extract header metadata from        #
# a file.                                                                      #
#                                                                              #
################################################################################

def extract_metadata(filename, Corners):
    strings = {
        'instrument number': action1,
        'Spectrum saved': action2,
#        'SWIR1 gain': action3,
#        'SWIR2 gain': action4,
        'GPS-Latitude': action5,
        'GPS-Longitude': action6,
        'GPS-UTC': action7
    }
    
    with open(filename) as file:
        list_of_actions = []
        for line in file:
            for search, action in strings.items():
                if search in line:
                    list_of_actions.append(action(line, Corners))
        return list_of_actions

################################################################################
#                                                                              #
# Extract spectrum and header information from an ASCII spectrum file.         #
# Create a Pandas dataframe with the result.                                   #
#                                                                              #
################################################################################

def load_spectrum_to_df(infile, li, Corners):
    
    p1 = subprocess.Popen(["grep", "-an", "^Wavelength", infile], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["cut", "-d:", "-f", "1"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    fdl,err = p2.communicate()
    firstDataLine = int(fdl)-1

#    inst, date_str, swir1_go, swir2_go, lat, lon = extract_metadata(infile, Corners)
    inst, date_str, lat, lon, utc_time = extract_metadata(infile, Corners)

    #swir1_gain = swir1_go[:3]
    #swir1_offset = swir1_go[-4:]
    #swir2_gain = swir2_go[:3]
    #swir2_offset = swir2_go[-4:]

    date_saved = datetime.datetime.strptime(date_str, '%m/%d/%Y at %H:%M:%S')

    # Test to see if GPS-UTC line is in hh:mm:ss format. If so, update the
    # time stamp to the GPS-based time
    try:
        dummy = datetime.datetime.strptime(utc_time, '%H:%M:%S')
        date_saved = date_saved.replace(hour=int(utc_time[:2]), 
                minute=int(utc_time[3:5]), second=int(utc_time[6:]))
    except ValueError:
        pass
    
    df = pd.read_csv(infile, skiprows=firstDataLine, delim_whitespace=True)
    filename = df.columns[1]
    df.rename({filename: 'radiance'}, axis=1, inplace=True)
    df['filename'] = filename
    df['date_saved'] = date_saved
    df['Latitude'] = lat
    df['Longitude'] = lon
    df['Line'] = li
    try:
        df['Spec_number'] = int(filename[-11:-8])
    except ValueError:
        df['Spec_number'] = int(filename[-6:-4])
    df['Inst_number'] = inst
    #df['SWIR1_gain'] = swir1_gain
    #df['SWIR1_offset'] = swir1_offset
    #df['SWIR2_gain'] = swir2_gain
    #df['SWIR2_offset'] = swir2_offset
    return df

################################################################################
#                                                                              #
# Load spectrum from ASD binary file                                           #
#                                                                              #
################################################################################

def load_ASD_binary(infile, li, Corners):

    # Read in raw ASD binary file
    rawSpec = ASD_reader.reader(infile)
    
    # Define channel numbers for spectral breaks between visnir, swir1 and
    # swir2 (normally at 1000 and 1800nm)
    break1 = int(rawSpec.md.splice1_wavelength - rawSpec.md.ch1_wave + 1)
    break2 = int(rawSpec.md.splice2_wavelength - rawSpec.md.ch1_wave + 1)
    
    # Define end channel of spectrum
    endChan = rawSpec.md.channels + 1
    
    # Integration time for calibration
    calGain0 = rawSpec.calibration_header[2][2] 

    # Gain of SWIR1 for calibration spectrum
    calGain1 = 2048 / rawSpec.calibration_header[2][3]

    # Gain of SWIR2 for calibration spectrum
    calGain2 = 2048 / rawSpec.calibration_header[2][4]

    # Intermediate calibration spectrum
    cal_rad = rawSpec.calibration_base*rawSpec.calibration_lamp / np.pi

    #
    # Create calibration spectrum by applying the breaks between sensors, with
    # the calibration gains
    #
    calSpec = cal_rad.copy()
    calSpec[:break1] = cal_rad[:break1] * calGain0 / rawSpec.calibration_fibre[:break1]
    calSpec[break1:break2] = cal_rad[break1:break2] * calGain1 / rawSpec.calibration_fibre[break1:break2]
    calSpec[break2:endChan] = cal_rad[break2:endChan] * calGain2 / rawSpec.calibration_fibre[break2:endChan]

    # Integration time of target spectrum
    specGain0 = rawSpec.md.integration_time

    # Gain of SWIR1 for target spectrum
    specGain1 = 2048 / rawSpec.md.swir1_gain

    # Gain of SWIR2 for target spectrum
    specGain2 = 2048 / rawSpec.md.swir2_gain

    #
    # Create radiance spectrum of target by applying breaks between sensors
    #
    radSpec = rawSpec.spec.copy()
    radSpec[:break1] = calSpec[:break1] * radSpec[:break1] / specGain0
    radSpec[break1:break2] = calSpec[break1:break2] * radSpec[break1:break2] / specGain1
    radSpec[break2:endChan] = calSpec[break2:endChan] * radSpec[break2:endChan] / specGain2
    
    #
    # Create dictionary which includes both wavelength and radiance columns
    #
    OutSpecDict = {'Wavelength': rawSpec.wavelengths.astype(int), 'radiance': radSpec}

    #
    # Create Pandas dataframe with Wavelength and radiance.
    #
    df = pd.DataFrame(OutSpecDict)

    # Add filename column
    df['filename'] = infile.split('/')[-1:][0]

    # Add time stamp column
    df['date_saved'] = pd.Timestamp(GPSTime(rawSpec))

    # Add latitude column
    latString = str(array.array('d', rawSpec.md.gps_data[16:24])[0])
    lat = int(latString[0:3])-float(latString[3:])/60
    df['Latitude'] = lat

    # Add longitude column
    lonString = str(array.array('d', rawSpec.md.gps_data[24:32])[0])
    lon = int(lonString[1:4])+float(lonString[4:])/60
    df['Longitude'] = lon

    # Add Altitude column
    alt = array.array('d', rawSpec.md.gps_data[32:40])[0]
    df['Altitude'] = alt

    # Add line number column
    df['Line'] = li

    # Add spectrum number column
    try:
        df['Spec_number'] = int(infile[-7:-4])
    except ValueError:
        df['Spec_number'] = int(infile[-6:-4])

    # Add Instrument number / calibration number column
    df['Inst_number'] = str(rawSpec.md.instrument_num)+'/'+str(rawSpec.md.calibration)

    #
    # The following lines could be added back in, if the information was
    # necessary
    #
    #df['SWIR1_gain'] = rawSpec.md.swir1_gain
    #df['SWIR1_offset'] = rawSpec.md.swir1_offset
    #df['SWIR2_gain'] = rawSpec.md.swir2_gain
    #df['SWIR2_offset'] = rawSpec.md.swir2_offset

    return df


################################################################################
#                                                                              #
# Get the date from the spectrum saved time stamp and get the time from the    #
# GPS data                                                                     #
#                                                                              #
################################################################################

def GPSTime(spectrum):
    GPSSum = sum(array.array('b', spectrum.md.gps_data).tolist())
    if  GPSSum == 0:
        DateAndTime = spectrum.md.save_time
    else:
        TimeBytes = array.array('b', spectrum.md.gps_data[43:46])
        TimeBytes.reverse()
        gps_time = datetime.time(TimeBytes[0], TimeBytes[1], TimeBytes[2])
        DateAndTime = datetime.datetime.combine(spectrum.md.save_time.date(), gps_time)
        time_diff = (DateAndTime - spectrum.md.save_time).total_seconds()

        # Test if time difference between GPS time and spectrum_saved time is
        # greater than 11 hours. If so, change the date by one day. This is to
        # catch edge-cases where one time stamp is just before midnight and the
        # other just after.
        #
        # If the ASD laptop is out of sync by more than 11 hours, then the
        # time stamps cannot be trusted anyway.
        #
        if time_diff < -39600:
            DateAndTime = DateAndTime + datetime.timedelta(days=1)
        elif time_diff > 39600:
            DateAndTime = DateAndTime - datetime.timedelta(days=1)

    return DateAndTime


################################################################################
#                                                                              #
# Loop through all spectrum files in "indir" and combine the resulting         #
# dataframes.                                                                  #
#                                                                              #
# For each 'line*' directory in 'indir', iterate through each file             #
# ending with 'suffix' and run 'load_spectrum_to_df'. Finally,                 #
# return a concatenated dataframe made up of all the individual                #
# dataframes.                                                                  #
#                                                                              #
################################################################################

def load_from_dir(indir, suffix, firstGoodLine, Corners):
    all_dfs = []
    numLines = len(range(firstGoodLine, len(glob.glob(indir+'line*'))+1))
    for li in range(firstGoodLine, len(glob.glob(indir+'line*'))+1):
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

            if suffix == 'asd':
                df = load_ASD_binary(infile, li, Corners)
            else:
                df = load_spectrum_to_df(infile, li, Corners)

            all_dfs.append(df)

    return pd.concat(all_dfs)
