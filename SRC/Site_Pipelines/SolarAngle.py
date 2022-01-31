#
# Astropy is used to determine the Solar angle
#
import astropy.coordinates as coord
from astropy.time import Time
import astropy.units as u

def solang(row):

    loc = coord.EarthLocation(lon=row['Longitude'] * u.deg,
                              lat=row['Latitude'] * u.deg)
    #timy0 = timei.to_pydatetime()
    timy = Time(row['date_saved'], format='datetime')
    
    altaz = coord.AltAz(location=loc, obstime=timy)
    sun = coord.get_sun(timy)

    return sun.transform_to(altaz).zen.degree

def add_solar(good_spectra, solang):
    #
    # Add Solar_angle column to good_panels Dataframe based on 350nm
    # wavelength only (to save processing time).
    #
    solzen = good_spectra[good_spectra['Wavelength']==350].apply(solang, axis=1)
    
    #
    # Create Pandas Series with date_saved column, with the same length as "solzen".
    #
    times = good_spectra[good_spectra['Wavelength']==350].date_saved
    
    #
    # Stop Pandas complaining about doing a copy for the follwing line
    #
    import pandas as pd
    pd.options.mode.chained_assignment = None  # default='warn'

    #
    # Loop through "good_panels" and change "Solar_angle" to appropriate value in
    # "solzen" for each date found in "times".
    #
    good_spectra['Solar_angle'] = 1.0
    
    SolCount = []
    for i in range(len(solzen.values)):
        for j in range(len(good_spectra[good_spectra.date_saved == times.values[i]])):
            SolCount.append(solzen.values[i])
    good_spectra.Solar_angle = SolCount

    return good_spectra

def solar_angle(good_panels, good_grounds, field_data):

    if (field_data[5] == 'Radiance') or (field_data[5] == 'Binary'):
        good_panels = add_solar(good_panels, solang)
        good_grounds = add_solar(good_grounds, solang)

    return good_panels, good_grounds
