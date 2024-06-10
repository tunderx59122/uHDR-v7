# uHDR: HDR image editing software
#   Copyright (C) 2022  remi cozot 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
# hdrCore project 2020-2022
# author: remi.cozot@univ-littoral.fr

# import
# ------------------------------------------------------------------------------------------
import numpy as np

# ------------------------------------------------------------------------------------------

# hueBarLch = buildLchColourData((75,75), (100,100), (0,360), (20,720), width='h', height='c')

def buildLchcolourData( L : tuple[float,float],
                        c : tuple[float, float],
                        h :tuple[float,float],
                        size : tuple[int,int],
                        width: str,
                        height:str) -> np.ndarray:


    colourData : np.ndarray= np.zeros((size[0], size[1],3))
    Lmin, Lmax = L if L[0] < L[1] else (L[1], L[0])
    cmin, cmax = c if c[0] < c[1] else (c[1], c[0])
    hmin, hmax = h

    xmin, xmax = 0, size[1]
    ymin, ymax = 0, size[0]

    if width=='L':
        if height=='c':
            #     +-------------------------------+
            #  c  |                               |
            #     +-------------------------------+
            #                Lightness
            for x in range(xmin,xmax):
                for y in range(ymin,ymax):
                    u, v = x/(xmax-1), y/(ymax-1)
                    Lu = Lmin*(1-u)+Lmax*u
                    cv = cmin*(1-v) + cmax*v
                    hh = (hmin+hmax)/2
                    colourData[y,x,:] = [Lu,cv,hh]
        elif height=='h':
            #     +-------------------------------+
            #  h  |                               |
            #     +-------------------------------+
            #                Lightness
            for x in range(xmin,xmax):
                for y in range(ymin,ymax):
                    u, v = x/(xmax-1), y/(ymax-1)
                    Lu = Lmin*(1-u)+Lmax*u
                    if hmin <= hmax:
                        hv = hmin*(1-v) + hmax*v
                    else:
                        # hmin = 340 / hmax=20 -> hmin = hmin-360 >> hmin = -20, hmax =20
                        hv = (hmin-360)*(1-v) + hmax*v
                        if hv < 0: hv = 360 +hv
                    cc = (cmin+cmax)/2
                    colourData[y,x,:] = [Lu,cc,hv]
    elif width=='c':
        if height=='L':
            #     +-------------------------------+
            #  L  |                               |
            #     +-------------------------------+
            #                chroma
            for x in range(xmin,xmax):
                for y in range(ymin,ymax):
                    u, v = x/(xmax-1), y/(ymax-1)
                    cu = cmin*(1-u) + cmax*u
                    Lv = Lmin*(1-v)+Lmax*v
                    hh = (hmin+hmax)/2
                    colourData[y,x,:] = [Lv,cu,hh]
        elif height=='h':
            #     +-------------------------------+
            #  h  |                               |
            #     +-------------------------------+
            #                chroma
            for x in range(xmin,xmax):
                for y in range(ymin,ymax):
                    u, v = x/(xmax-1), y/(ymax-1)
                    cu = cmin*(1-u) + cmax*u
                    if hmin <= hmax:
                        hv = hmin*(1-v) + hmax*v
                    else:
                        # hmin = 340 / hmax=20 -> hmin = hmin-360 >> hmin = -20, hmax =20
                        hv = (hmin-360)*(1-v) + hmax*v
                        if hv < 0: hv = 360 +hv
                    LL = (Lmin+Lmax)/2
                    colourData[y,x,:] = [LL,cu,hv]
    elif width == 'h':
        if height=='L':
            #     +-------------------------------+
            #  L  |                               |
            #     +-------------------------------+
            #                hue
            for x in range(xmin,xmax):
                for y in range(ymin,ymax):
                    u, v = x/(xmax-1), y/(ymax-1)
                    if hmin <= hmax:
                        hu = hmin*(1-u) + hmax*u
                    else:
                        # hmin = 340 / hmax=20 -> hmin = hmin-360 >> hmin = -20, hmax =20
                        hu = (hmin-360)*(1-u) + hmax*u
                        if hu < 0: hv = 360 +hu
                    Lv = Lmin*(1-v)+Lmax*v
                    cc = (cmin+cmax)/2
                    colourData[y,x,:] = [Lv,cc,hu]
        elif height=='c':
            #     +-------------------------------+
            #  c  |                               |
            #     +-------------------------------+
            #                hue
            for x in range(xmin,xmax):
                for y in range(ymin,ymax):
                    u, v = x/(xmax-1), y/(ymax-1)
                    if hmin <= hmax:
                        hu = hmin*(1-u) + hmax*u
                    else:
                        # hmin = 340 / hmax=20 -> hmin = hmin-360 >> hmin = -20, hmax =20
                        hu = (hmin-360)*(1-u) + hmax*u
                        if hu < 0: hv = 360 +hu
                    cv = cmin*(1-v)+cmax*v
                    LL = (Lmin+Lmax)/2
                    colourData[y,x,:] = [LL,cv,hu]

    return colourData

