from __future__ import annotations
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
import os, json
from hdrCore.Exif import Exif
# ------------------------------------------------------------------------------------------
# --- class Tags ---------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = False
# ------------------------------------------------------------------------------------------ 
class Jexif: 
    @staticmethod
    def load(imageDir: str, imageFilename: str, extraDir : str) -> dict[str, str]:
        # check if extra '.uHDR' dir exist
        extraPath = os.path.join(imageDir, extraDir) 
        if os.path.isdir(extraPath):
            exifFilename= os.path.join(imageDir,extraDir,imageFilename[:-3]+'jexif') 
            if os.path.exists(exifFilename):
                with open(exifFilename) as exifFile:
                    jexif : dict[str, str] =  json.load(exifFile)
                    return jexif
            else: 
                rawExif : dict[str, str] | None = Exif.readExif(imageDir,imageFilename)
                if rawExif:
                    jexif : dict[str, str] = Exif.recoverExifData(rawExif) 
                    
                    # save jexif file
                    exifFilename= os.path.join(imageDir,extraDir,imageFilename[:-3]+'jexif')
                    with open(exifFilename, 'w') as exifFile:
                        json.dump(jexif, exifFile)                   
                    return jexif
        return {"Color Space": "unkwown", "Bits Per Sample": "-1", "Type": "unkwown", "Size": "-1 x -1"} # default value

    @staticmethod
    def toTuple(exifDict: dict[str, str]) -> tuple[tuple[int,int], str, str, int] :
        size : tuple[int,int] = (int(exifDict['Size'].split('x')[0]),int(exifDict['Size'].split('x')[-1]))
        colorSpace : str = exifDict['Color Space']
        type : str = exifDict['Type']
        bps : int = int(exifDict['Bits Per Sample'])
        return (size,colorSpace,type,bps)