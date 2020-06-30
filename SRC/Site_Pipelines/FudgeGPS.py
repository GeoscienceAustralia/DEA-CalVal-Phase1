import numpy as np
import math
#
# If there are no GPS coordinates in the header, then fudge them
# based on the extents of the field site (Corners: format = SE, SW, NE, NW).
#
def fudge_gps(ground_brdf, Corners, RockWalk, StartCorner):
    if Corners == [0, 0, 0, 0, 0, 0, 0, 0]:
        print('Assuming good GPS Coordinates, continuing...')
    else:
        print('No good GPS Coordinates found, fudging...')
        if StartCorner == 'NE':
            SpecHeight = (Corners[0]-Corners[4])
            SpecWidth = (Corners[1]-Corners[5])
            LineHeight = (Corners[6]-Corners[4])
            LineWidth = (Corners[7]-Corners[5])
        elif StartCorner == 'SE':
            SpecHeight = (Corners[4]-Corners[0])
            SpecWidth = (Corners[5]-Corners[1])
            LineHeight = (Corners[2]-Corners[0])
            LineWidth = (Corners[3]-Corners[1])
        elif StartCorner == 'NW':
            SpecHeight = (Corners[2]-Corners[6])
            SpecWidth = (Corners[3]-Corners[7])
            LineHeight = (Corners[4]-Corners[6])
            LineWidth = (Corners[5]-Corners[7])
        elif StartCorner == 'SW':
            SpecHeight = (Corners[6]-Corners[2])
            SpecWidth = (Corners[7]-Corners[3])
            LineHeight = (Corners[2]-Corners[0])
            LineWidth = (Corners[3]-Corners[1])
        else:
            print('Badly formatted "StartCorner". Should be one of NE, NW, SE, SW.')

        numLines = len(ground_brdf['Line'].unique())
        LineHeightSep = LineHeight/(numLines-1)
        LineWidthSep = LineWidth/(numLines-1)
        #print("SpecHeight = ", 111319.9*SpecHeight,
        #      "m\nSpecWidth = ", 111319.9*SpecWidth,
        #      "m\nLineHeight = ", 111319.9*LineHeight,
        #      "m\n LineWidth = ", 111319.9*LineWidth,
        #      "m\nLineHeightSep = ", 111319.9*LineHeightSep,
        #      "m\nLineWidthSep = ", 111319.9*LineWidthSep,
        #      "m\nnumLines = ", numLines)

        seqLine = 0
        for lineCount in ground_brdf['Line'].unique():
            seqLine += 1
                
            temp = ground_brdf[ground_brdf['Line']==lineCount]

            numSpectra = len(temp['Spec_number'].unique())
            SpecWidthSep = SpecWidth/(numSpectra-1)
            SpecHeightSep = SpecHeight/(numSpectra-1)
    
            if RockWalk == True:
                if lineCount % 2 == 1:
                    seqSpec = 0
                else:
                    seqSpec = numSpectra
            else:
                seqSpec = 0

            for specCount in temp['Spec_number'].unique():
                if RockWalk == True:
                    if lineCount % 2 == 1:
                        seqSpec += 1
                    else:
                        seqSpec -= 1
                else:
                    seqSpec += 1
    
                if StartCorner == 'SE':
                    fudgeLat = Corners[0]+(LineHeightSep*seqLine)+(SpecHeightSep*seqSpec)
                    fudgeLon = Corners[1]+(LineWidthSep*seqLine)+(SpecWidthSep*seqSpec)
                if StartCorner == 'SW':
                    fudgeLat = Corners[2]+(LineHeightSep*seqLine)+(SpecHeightSep*seqSpec)
                    fudgeLon = Corners[3]+(LineWidthSep*seqLine)+(SpecWidthSep*seqSpec)
                if StartCorner == 'NE':
                    fudgeLat = Corners[4]+(LineHeightSep*seqLine)+(SpecHeightSep*seqSpec)
                    fudgeLon = Corners[5]+(LineWidthSep*seqLine)+(SpecWidthSep*seqSpec)
                if StartCorner == 'NW':
                    fudgeLat = Corners[6]+(LineHeightSep*seqLine)+(SpecHeightSep*seqSpec)
                    fudgeLon = Corners[7]+(LineWidthSep*seqLine)+(SpecWidthSep*seqSpec)
    
                ground_brdf.at[ground_brdf[np.logical_and(ground_brdf['Line']==lineCount, ground_brdf['Spec_number']==specCount)].index, 'Latitude'] = fudgeLat
                ground_brdf.at[ground_brdf[np.logical_and(ground_brdf['Line']==lineCount, ground_brdf['Spec_number']==specCount)].index, 'Longitude'] = fudgeLon
    
    return ground_brdf
