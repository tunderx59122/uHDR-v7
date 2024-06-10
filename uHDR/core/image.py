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

from core.colourSpace import ColorSpace
from copy import deepcopy
import numpy as np, os, colour
import skimage.transform

# ------------------------------------------------------------------------------------------

debug : bool = True

# -----------------------------------------------------------------------------
def filenamesplit(filename):
    """retrieve path, name and extension from a filename.

    @Args:
        filename (str,Required): filename
            
    @Returns:
        (str,str,str): (path,name,ext)
            
    @Example:
        filenamesplit("./dir0/dir1/name.ext") returns ("./dir0/dir1/","name","ext")
    """
    
    path, nameWithExt = os.path.split(filename)
    splits = nameWithExt.split('.')
    ext = splits[-1].lower()
    name = '.'.join(splits[:-1])
    return (path,name,ext)


# ------------------------------------------------------------------------------------------
# --- class ImmageFiles(QObject) -----------------------------------------------------------
# ------------------------------------------------------------------------------------------
class Image:
    """color data  +  color space + hdr"""
    # constructor
    # -----------------------------------------------------------------
    def __init__(self:Image, data: np.ndarray, space: ColorSpace = ColorSpace.sRGB, isHdr: bool = False):

        self.cSpace : ColorSpace = space
        self.cData : np.ndarray = data
        self.hdr : bool = isHdr
    
    # methods
    # -----------------------------------------------------------------
    def __repr__(self: Image) -> str:
        y, x, c =  self.cData.shape
        res : str =  '-------------------    Image   -------------------------------'
        res += f'\n size: {x} x {y} x {c} '
        res += f'\n colourspace: {self.cSpace.name}'
        res += f'\n hdr: {self.hdr}'
        res +=  '\n-------------------  Image End -------------------------------'
        return res
    # -----------------------------------------------------------------
    def write(self: Image, fileName : str):
        """write image to system."""

        colour.write_image((self.cData*255.0).astype(np.uint8), fileName,  bit_depth='uint8', method= 'Imageio')
    # -----------------------------------------------------------------
    def buildThumbnail(self: Image, maxSize :int= 800) -> Image:
        """build a thumbnail image."""
        
        y, x, _ =  self.cData.shape
        factor : int = maxSize/max(y,x)
        if factor<1:
            thumbcData = skimage.transform.resize(self.cData, (int(y * factor),int(x*factor) ))

            return Image(thumbcData, self.cSpace, self.hdr)
        else:
            return deepcopy(self)


    # static methods
    # -----------------------------------------------------------------
    @staticmethod
    def read(fileName : str) -> Image:
        """read image from system."""
        img : Image 
        path, name, ext = filenamesplit(fileName)
        if os.path.exists(fileName):
            if ext == "jpg" :
                imgData :  np.ndarray = colour.read_image(fileName, bit_depth='float32', method= 'Imageio')
                img = Image(imgData, ColorSpace.sRGB, False)
        else:
            img = Image(np.ones((600,800,3))*0.50, ColorSpace.sRGB, False)
        return img
    # -----------------------------------------------------------------
