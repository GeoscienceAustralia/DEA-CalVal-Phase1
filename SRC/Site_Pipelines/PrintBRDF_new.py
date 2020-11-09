def print_brdf(alldata, field_data):

    #
    # Look for Collection Upgrade version in field_data
    # Should be like 'C5' or 'C6'. If it doesn't exist, set it to 'C5'.
    #
    try:
        CNum = field_data[7]
    except IndexError:
        CNum = 'C5'
    
    with open('tempfile.sh', 'w') as tempfile:
        tempfile.write("!#/bin/bash\n")
        tempfile.write("cd /g/data/up71/projects/CalVal_Phase1/brdf\n")
        tempfile.write("source module_")
        tempfile.write(CNum)
        tempfile.write(".sh\n")
        tempfile.write("sed -i \"40s/.*/        self.acquisition_datetime = dateutil.parser.parse(\'")
        tempfile.write(str(alldata['date_saved'].iloc[0]))
        tempfile.write("')/\" retrieve_brdf_")
        tempfile.write(CNum)
        tempfile.write(".py\n")
        tempfile.write("sed -i \"43s/.*/        bbox = geopandas.GeoDataFrame({'geometry': [box(")
        tempfile.write(str(alldata['Longitude'].min()))
        tempfile.write(", ")
        tempfile.write(str(alldata['Latitude'].min()))
        tempfile.write(", ")
        tempfile.write(str(alldata['Longitude'].max()))
        tempfile.write(", ")
        tempfile.write(str(alldata['Latitude'].max()))
        tempfile.write(")]})/\" retrieve_brdf_")
        tempfile.write(CNum)
        tempfile.write(".py\n")
        tempfile.write("python retrieve_brdf_")
        tempfile.write(CNum)
        tempfile.write(".py > temp.txt ; awk -f format_Sent.awk temp.txt\n")

    exec(open('tempfile.sh').read())
