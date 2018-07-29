import numpy as np
import math
#
# If there are no GPS coordinates in the header, then fudge them
# based on the extents of the field site (Corners: format = SE, SW, NE, NW).
#
def fudge_gps(ground_brdf, Corners, RockWalk):
    if Corners == [0, 0, 0, 0, 0, 0, 0, 0]:
        print('Assuming good GPS Coordinates, continuing...')
    else:
        print('No good GPS Coordinates found, fudging...')
        SpecHeight = (Corners[2]-Corners[0])
        SpecWidth = (Corners[3]-Corners[1])
        LineHeight = (Corners[4]-Corners[0])
        LineWidth = (Corners[5]-Corners[1])

        numLines = len(ground_brdf['Line'].unique())
        LineHeightSep = LineHeight/(numLines-1)
        LineWidthSep = LineWidth/(numLines-1)

        seqLine = 0
        for lineCount in ground_brdf['Line'].unique():
            seqLine += 1

            temp = ground_brdf[ground_brdf['Line']==lineCount]

            numSpectra = len(temp['Spec_number'].unique())
            SpecWidthSep = SpecWidth/(numSpectra-1)
            SpecHeightSep = SpecHeight/(numSpectra-1)
    
            if RockWalk == True:
                if lineCount % 2 == 0:
                    seqSpec = 0
                else:
                    seqSpec = numSpectra
            else:
                seqSpec = 0

            for specCount in temp['Spec_number'].unique():
                if RockWalk == True:
                    if lineCount % 2 == 0:
                        seqSpec += 1
                    else:
                        seqSpec -= 1
                else:
                    seqSpec += 1
    
                fudgeLat = Corners[0]+(LineHeightSep*seqLine)+(SpecHeightSep*seqSpec)
                fudgeLon = Corners[1]+(LineWidthSep*seqLine)+(SpecWidthSep*seqSpec)
    
                ground_brdf.at[ground_brdf[np.logical_and(ground_brdf['Line']==lineCount, ground_brdf['Spec_number']==specCount)].index, 'Latitude'] = fudgeLat
                ground_brdf.at[ground_brdf[np.logical_and(ground_brdf['Line']==lineCount, ground_brdf['Spec_number']==specCount)].index, 'Longitude'] = fudgeLon
    
    return ground_brdf
