def scale_panels(slope, intercept, coszenith, gpt, good_panels):

    ratio = gpt['Averaged_Panels']/(slope*(coszenith)+intercept)

    for i in range(len(gpt['Averaged_Panels'])):
        good_panels.radiance[good_panels['date_saved'] == gpt['date_saved'].iloc[i]] = \
            good_panels.radiance[good_panels['date_saved'] == gpt['date_saved'].iloc[i]]/ratio.iloc[i]

    return good_panels
