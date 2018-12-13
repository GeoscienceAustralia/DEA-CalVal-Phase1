import numpy as np
import pandas as pd
import csv


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
def apply_weights(f_name, all_refls, sat_resp, field_data):

    if field_data[3] == 'Landsat8':
        ls_band = get_spectrum_curve(f_name)
        s2_band = get_spectrum_curve(sat_resp['Sentinel2a'])
    else:
        ls_band = get_spectrum_curve(sat_resp['Landsat8'])
        s2_band = get_spectrum_curve(f_name)

    ls_result = []
    s2_result = []
    wave_length = np.array(all_refls.index, dtype='float64')
    for col in all_refls.columns:
        source_x = np.vstack([wave_length, np.array(all_refls[col], dtype='float64')]).T
        ls_result.append(field_int_curve(source_x, ls_band))
        s2_result.append(field_int_curve(source_x, s2_band))
    ls_result_df = pd.DataFrame(ls_result)
    s2_result_df = pd.DataFrame(s2_result)
    ls_result_df.columns = list(ls_band.keys())
    s2_result_df.columns = list(s2_band.keys())

    return ls_result_df, s2_result_df, ls_band, s2_band
