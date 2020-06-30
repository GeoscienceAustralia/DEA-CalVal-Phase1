from datetime import datetime, timedelta
import pandas as pd
import glob, os, subprocess


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

#
# Based on action functions defined above, extract header metadata from
# a file.
#
def extract_metadata(filename, Corners):
    strings = {
        'instrument number': action1,
        'Spectrum saved': action2,
#        'SWIR1 gain': action3,
#        'SWIR2 gain': action4,
        'GPS-Latitude': action5,
        'GPS-Longitude': action6
    }
    
    with open(filename) as file:
        list_of_actions = []
        for line in file:
            for search, action in strings.items():
                if search in line:
                    list_of_actions.append(action(line, Corners))
        return list_of_actions

#
### Extract spectrum and header information from a spectrum file. 
### Create a Pandas dataframe with the result.
#
def load_spectrum_to_df(infile, li, Corners):
    
    p1 = subprocess.Popen(["grep", "-an", "^Wavelength", infile], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["cut", "-d:", "-f", "1"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    fdl,err = p2.communicate()
    firstDataLine = int(fdl)-1

#    inst, date_str, swir1_go, swir2_go, lat, lon = extract_metadata(infile, Corners)
    inst, date_str, lat, lon = extract_metadata(infile, Corners)

    #swir1_gain = swir1_go[:3]
    #swir1_offset = swir1_go[-4:]
    #swir2_gain = swir2_go[:3]
    #swir2_offset = swir2_go[-4:]

    date_saved = datetime.strptime(date_str, '%m/%d/%Y at %H:%M:%S')
    
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

#
### Loop through all spectrum files in "indir" and combine the resulting dataframes.
#
# For each 'line*' directory in 'indir', iterate through each file
# ending with 'suffix' and run 'load_spectrum_to_df'. Finally,
# return a concatenated dataframe made up of all the individual
# dataframes.
#
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

            df = load_spectrum_to_df(infile, li, Corners)
            all_dfs.append(df)
    return pd.concat(all_dfs)
