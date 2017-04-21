#!/usr/bin/env python
#
# CIE 1931 Color space:
# https://en.wikipedia.org/wiki/CIE_1931_color_space
#
# Reference color chart:
# https://www.ledtuning.nl/sites/all/modules/modledtuning/cie/CIE1931_ledtuning.png
# http://www.developers.meethue.com/sites/default/files/gamut_0.png
#
# Online color calculator:
# http://www.brucelindbloom.com/index.html?ColorCalculator.html
# 
# RGB Matrices:
# http://www.brucelindbloom.com/index.html?Eqn_RGB_XYZ_Matrix.html
# 

import math
import sys

def rgb2XYZ(r, g, b, gamma):
    print ("rgb -> XYZ")
    print("RGB input: %s %s %s" % (int(r*255), int(g*255), int(b*255) ))
    print("RGB input: %s %s %s" % (r, g, b ))

    # GAMMA CORRECTION
    if (gamma > 0.0):
        print ("With gamma correction %s" % (gamma))
        if (r <= 0.04045):
            r = r/12.92
        else:
            r = float( math.pow((r+0.055)/1.055, gamma) )

        if (g <= 0.04045):
            g = g/12.92
        else:
            g = float( math.pow((g+0.055)/1.055, gamma) )

        if (b <= 0.04045):
            b = b/12.92
        else:
            b = float( math.pow((b+0.055)/1.055, gamma) )
    

    # RGB to XYZ
    # Note: Y in XYZ is the "percieved lluminance"

    # CIE RGB Ref White E
    X = r * 0.4887180 + g * 0.3106803 + b * 0.2006017
    Y = r * 0.1762044 + g * 0.8129847 + b * 0.0108109
    Z = r * 0.0000000 + g * 0.0102048 + b * 0.9897952

    print ("XYZ output: %s %s %s \n" % (X,Y,Z))
    return X, Y, Z


def XYZ2xyY(X, Y, Z):
    print ("XYZ -> xyY")
    print ("XYZ input: %s %s %s" % (X, Y, Z))
    # check if RGB was not 0 0 0
    if ((X + Y + Z) != 0):
        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)
    else:
    # If RGB was 0 0 0 we set xy to reference white color here
    # and luminance Y will stay 0 in xyY
        Xr = 0.964221
        Yr = 1.0
        Zr = 0.825211

        x = Xr / (Xr + Yr + Zr)
        y = Yr / (Xr + Yr + Zr)

    print ("xyY output: %s %s %s \n" % (x,y,Y))
    return x, y, Y


def xyY2XYZ(xyy_x, xyy_y, xyy_Y):
    print ("xyY -> XYZ")
    print("xyY input: %s %s %s" % (x, y, Y))

    # TODO
    # if ther's no Y value known we assume Y = ???


    # avoid division by zero - PROBABLY NOT NEEDED
    #if xyy_Y == 0.0:
    #    XYZ_X = 0.0
    #    XYZ_Y = 0.0
    #    XYZ_Z = 0.0
    #else:
    XYZ_X = (float(xyy_x) * float(xyy_Y)) / float(xyy_y)
    XYZ_Y = float(xyy_Y)
    XYZ_Z = ((1.0 - float(xyy_x) - float(xyy_y)) * XYZ_Y) / float(xyy_y)

    print ("XYZ output: %s %s %s\n" % (XYZ_X, XYZ_Y, XYZ_Z))
    return XYZ_X, XYZ_Y, XYZ_Z

def XYZ2rgb(X, Y, Z, gamma):
    print ("XYZ -> RGB")
    print ("XYZ input: %s %s %s" % (X, Y, Z))

    # CIE RGB Ref White E
    R = X *  2.3706743 + Y * -0.9000405 + Z * -0.4706338
    G = X * -0.5138850 + Y *  1.4253036 + Z *  0.0885814
    B = X *  0.0052982 + Y * -0.0146949 + Z *  1.0093968

    # GAMMA CORRECTION
    if (gamma > 0.0):
        print ("With gamma correction %s" % (gamma))
        if( R > 0.0031308 ):
            R = 1.055 * math.pow( R, 1 / gamma ) - 0.055
        else:
            R *= 12.92

        if( G > 0.0031308 ):
            G = 1.055 * math.pow( G, 1 / gamma ) - 0.055
        else:
            G *= 12.92

        if( B > 0.0031308 ):
            B = 1.055 * math.pow( B, 1 / gamma ) - 0.055
        else:
            B *= 12.92


        # fixing the RGB values for allowed min and max values
        if (R < 0.1):
            R = 0.0
        elif (R > 1.0):
            R = 1.0

        if (G < 0.1):
            G = 0.0
        elif (G > 1.0):
            G = 1.0

        if (B < 0.1):
            B = 0.0
        elif (B > 1.0):
            B = 1.0

    # changing the printing format of 1e-6 numbers
    print ("RGB output: %s %s %s" % ('{:f}'.format(R), '{:f}'.format(G), '{:f}'.format(B)))
    print ("RGB output: %s %s %s" % (int(R*255.0), int(G*255.0), int(B*255.0)))
    return R, G, B


################################################################
## MAIN STUFF
################################################################

# Gamma correction
# 0.0 = NO CORRECTION
gamma_correction = 0.0

#print len(sys.argv)
#print sys.argv

# if there are any arguments
if len(sys.argv) > 1:
    # if first argument is RGB and there are additional R G B values
    if 'rgb' == sys.argv[1].lower() and len(sys.argv) == 5:
        #check if arguments are within 0-255 range
        for value in sys.argv[2:5]:
            if 0 <= int(value) <= 255:
                pass
            else:
                sys.exit("Value %s out of range 0-255 \nCheck your RGB input values" % (value))

        R = sys.argv[2]
        G = sys.argv[3]
        B = sys.argv[4]
        print "Converting RGB [%s %s %s] to xyY" % (R, G, B)

        R = float(R)/255
        G = float(G)/255
        B = float(B)/255

        X, Y, Z = rgb2XYZ(R, G, B, gamma_correction)
        x, y, Y = XYZ2xyY(X, Y, Z)

        print("------------------------------------")
        print("Converting xyY back to RGB for check")
        print("------------------------------------")

        X, Y, Z = xyY2XYZ(x, y, Y)
        R, G, B = XYZ2rgb(X, Y, Z, gamma_correction)

    # if first argument is xyY and there are additional x y Y values
    if 'xyy' == sys.argv[1].lower() and len(sys.argv) == 5:
        #check if arguments are within 0.0 - 1.0 range
        for value in sys.argv[2:5]:
            if 0.0 <= float(value) <= 1.0:
                pass
            else:
                sys.exit("Value %s out of range 0.0 - 1.0 \nCheck your xyY input values" % (value))

        x = sys.argv[2]
        y = sys.argv[3]
        Y = sys.argv[4]

        print "Converting xyY [%s %s %s] to RGB" % (x, y, Y)

        x = float(x)
        y = float(y)
        Y = float(Y)

        X, Y, Z = xyY2XYZ(x, y, Y)
        R, G, B = XYZ2rgb(X, Y, Z, gamma_correction)
                

sys.exit()

# THESE 3 components make the Y at max Brightness
# We need to figure out, how to calculate the CurrentLevel to these
Yr = 0.176204
Yg = 0.813058
Yb = 0.010811
