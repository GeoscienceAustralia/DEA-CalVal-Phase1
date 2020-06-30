import numpy as np

def scale_grounds(good_panels, good_grounds, slope, intercept, field_data):

    if field_data[5] == 'Radiance':
        count=0
        for i in good_panels.Line.unique():
            count+=1
            #
            # mean_panel_fit is a single number. The line-averaged panel Solar angle is determined (LAPSA). LAPSA is
            # then fed through the line of best fit with form slope*LAPSA + intercept = mean_panel_fit.
            #
            mean_panel_fit = slope*(np.cos(np.deg2rad(good_panels[good_panels['Line']==i].Solar_angle.mean())))+intercept
        
            #
            # good_grounds_fit is a pandas Series of the line of best fit values for each individual ground spectrum within
            # a single line.
            #
            good_grounds_fit = slope*(np.cos(np.deg2rad(good_grounds[good_grounds.Line==i].Solar_angle)))+intercept
        
            #
            # pan_ground_ratio is the ratio of mean_panel_fit and good_grounds_fit, which is the multiplicative factor
            # needed to apply to the ground spectra to correct for insolation.
            #
            if count==1:
                pan_ground_ratio = mean_panel_fit/good_grounds_fit
            else:
                pan_ground_ratio = pan_ground_ratio.append(mean_panel_fit/good_grounds_fit)
        #
        # Apply the multiplicative scaling factor to the ground spectra in good_grounds
        #
        good_grounds.radiance = good_grounds.radiance.multiply(pan_ground_ratio)

    return good_grounds
