def scale_panels(slope, intercept, coszenith, gpt, good_panels, field_data):

    if field_data[5] == 'Radiance':
        ratio = gpt['Averaged_Panels']/(slope*(coszenith)+intercept)

        PanCount = []
    
        for i in range(len(gpt['Averaged_Panels'])):
            for j in range(len(good_panels[good_panels.date_saved == gpt['date_saved'].iloc[i]])):
                PanCount.append(ratio.iloc[i])
    
        good_panels.radiance = good_panels.radiance/PanCount
    
#        for i in range(len(gpt['Averaged_Panels'])):
#            good_panels.radiance[good_panels['date_saved'] == gpt['date_saved'].iloc[i]] = \
#                good_panels.radiance[good_panels['date_saved'] == gpt['date_saved'].iloc[i]]/ratio.iloc[i]

    return good_panels
