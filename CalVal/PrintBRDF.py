def print_brdf(alldata, field_data):

    #
    # Look for Collection Upgrade version in field_data
    # Should be like 'C5' or 'C6'. If it doesn't exist, set it to 'C5'.
    #
    try:
        CNum = field_data[7]
    except IndexError:
        CNum = 'C5'
    
    print("#################################################################################\n# Copy and paste the following into a terminal window on VDI for Landsat 8 data #\n#################################################################################\n")
    print("source module_"+CNum+".sh")
    print("sed -i \"40s/.*/        self.acquisition_datetime = dateutil.parser.parse('",alldata['date_saved'].iloc[0],"')/\" retrieve_brdf_"+CNum+".py", sep='')
    print("sed -i \"43s/.*/        bbox = geopandas.GeoDataFrame({'geometry': [box(",alldata['Longitude'].min(),", ", alldata['Latitude'].min(),", ", alldata['Longitude'].max(),", ", alldata['Latitude'].max(),")]})/\" retrieve_brdf_"+CNum+".py", sep='')
    print("python retrieve_brdf_"+CNum+".py > temp.txt ; awk -f format_Sent.awk temp.txt")
    print("")

