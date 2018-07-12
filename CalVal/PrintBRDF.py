def print_brdf(alldata, field_data):

    if field_data[3] == 'Landsat8':
        print("#################################################################################\n# Copy and paste the following into a terminal window on VDI for Landsat 8 data #\n#################################################################################\n")
        print("source module.sh")
        print("sed -i \"34s/.*/        setattr(self, 'acquisition_datetime', dateutil.parser.parse('",alldata['date_saved'].iloc[0],"'))/\" retrieve_brdf.py", sep='')
        print("sed -i \"37s/.*/        bbox = geopandas.GeoDataFrame({'geometry': [box(",alldata['Longitude'].min(),", ", alldata['Latitude'].min(),", ",
              alldata['Longitude'].max(),", ", alldata['Latitude'].max(),")]})/\" retrieve_brdf.py", sep='')
        print("python retrieve_brdf.py > temp.txt ; awk -f format.awk temp.txt")
        print("")
    
    elif field_data[3] == 'Sentinel2a' or field_data[3] == 'Sentinel2b':
        print("##################################################################################\n# Copy and paste the following into a terminal window on VDI for Sentinel 2 data #\n##################################################################################\n")
        print("source module.sh")
        print("sed -i \"34s/.*/        setattr(self, 'acquisition_datetime', dateutil.parser.parse('",alldata['date_saved'].iloc[0],"'))/\" retrieve_brdf.py", sep='')
        print("sed -i \"37s/.*/        bbox = geopandas.GeoDataFrame({'geometry': [box(",alldata['Longitude'].min(),", ", alldata['Latitude'].min(),", ",
              alldata['Longitude'].max(),", ", alldata['Latitude'].max(),")]})/\" retrieve_brdf.py", sep='')
        print("python retrieve_brdf.py > temp.txt ; awk -f format_Sent.awk temp.txt")
        print("")
        
    else:
        print('Satellite name should be one of Landsat8 or Sentinel 2a/b. I got', field_data[3])
