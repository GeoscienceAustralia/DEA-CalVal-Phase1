#
### Rename the first spectrum in ALL/GOOD panels to the correct name
#
# Rather than just "radiance", it will be named something like radiance1-0
# for the zeroth spectrum in the first line, for example.
#
def spec_rename(good_panel_spec, good_grounds_spec, firstGoodLine, firstGoodPanelSpec, firstGoodGroundSpec, field_data):

    if field_data[5] == 'Radiance':
        gps_new_name = 'radiance'+str(firstGoodLine)+"-"+str(firstGoodPanelSpec)
        ggs_new_name = 'radiance'+str(firstGoodLine)+"-"+str(firstGoodGroundSpec)

        good_panel_spec.rename(columns={'radiance': gps_new_name}, inplace=True)
        good_grounds_spec.rename(columns={'radiance': ggs_new_name}, inplace=True)
