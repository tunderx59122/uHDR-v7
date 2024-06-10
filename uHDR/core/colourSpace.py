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
from __future__ import annotations
import numpy as np
import colour
from enum import Enum
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------
# --- class ImmageFiles(QObject) -----------------------------------------------------------
# ------------------------------------------------------------------------------------------
class ColorSpace(Enum):
    """class color space names enumerate."""
    No    = 0
    RGB   = 1
    sRGB  = 2
    scRGB = 3
    Lab   = 4
    Luv   = 5
    IPT   = 6
    Jzazbz= 7
    XYZ   = 8



# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
def Lch_to_sRGB(Lch :np.ndarray,apply_cctf_encoding :bool=True, clip : bool=False) -> np.ndarray:
    """convert pixel array from Lch to sRGB colorspace.

    Args:
        Lch (numpy.ndarray, Required): array of pixels in Lab colourspace.
        apply_cctf_encoding (boolean, Optionnal): True to encode with sRGB cctf encoding function.
        clip (boolean, Optionnal): False do not clip values beyond colourspace limits (RGB values < 0 or RGB values > 1).
            
    Returns:
        (numpy.ndarray): array of pixels in sRGB colorspace.
    """
    Lab : np.ndarray = colour.LCHab_to_Lab(Lch)
    XYZ  :np.ndarray = colour.Lab_to_XYZ(Lab, illuminant=np.array([ 0.3127, 0.329 ]))
    RGB : np.ndarray = colour.XYZ_to_sRGB(
        XYZ, illuminant=np.array([ 0.3127, 0.329 ]), 
        chromatic_adaptation_transform='CAT02', 
        apply_cctf_encoding = apply_cctf_encoding)
    if clip:
        RGB[RGB<0] = 0
        RGB[RGB>1] = 1
    return RGB
# ------------------------------------------------------------------------------------------
