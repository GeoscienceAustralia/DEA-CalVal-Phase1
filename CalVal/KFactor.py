import pandas as pd


#
### Define the K-factor
#
# This reads a standard file with a response curve for the detector, given an
# ideally white surface. Then "k_f" is defined for the K-factor.
def k_factor(panel_dir, in_panel):
    k_f = pd.read_csv(panel_dir + in_panel, skiprows=5, delim_whitespace=True)
    # Set index to wavelength
    k_f.set_index("Wavelength", inplace = True) 
    
    return k_f
