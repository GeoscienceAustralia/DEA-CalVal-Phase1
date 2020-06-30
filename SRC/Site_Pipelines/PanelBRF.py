import pandas as pd
import numpy as np


def Panel_BRF(good_panels, field_data):

    if field_data[5] == 'Radiance':
        #
        # Read in Panel BRF factors from csv and calculate mean
        #
        dat = pd.read_csv('/g/data/up71/projects/CalVal_Phase1/GitRepoFiles/SRT3BRDFa.csv')
        dat.set_index('Wavelength', inplace=True)
        mean = dat.mean()
        
        #
        # Multiply the radiance by a correction, based on a linear interpolation of
        # the Panel BRF factors, as a function of the Solar angle. The factor of
        # 1.005230 comes from the average of the correction at 45 degrees, which is
        # used to normalise so that the correction at 45 degrees is = 1.
        #
        good_panels.radiance = good_panels.radiance * 1.005230 / \
                               np.interp(good_panels.Solar_angle, 
                               np.array(mean.index, dtype='float64'), mean.values)

        return good_panels
    else:
        return good_panels
