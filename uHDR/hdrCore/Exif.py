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
from typing_extensions import Self
import os, subprocess
# ------------------------------------------------------------------------------------------
# --- class Exif ---------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = True
class Exif:    
    @staticmethod
    def readExif(imagePath: str ,filename: str) -> dict[str,str]|None:
        """ returns a dict containing exif data.
        """
        exifDict = {}
        file : str = os.path.join(imagePath, filename)

        if debug : print(f'EXif.readExif({imagePath},{filename}) -> {file}')

        if os.path.isfile(file): # check if filename exists
            if os.path.isfile('exiftool.exe'):# reading metadata with exiftool
                try:
                    exifdata : str = subprocess.check_output(['exiftool.exe','-a',file],
                        shell=True, universal_newlines=True,
                        stdin=subprocess.PIPE, stderr=subprocess.PIPE)
                    exifdataLines :list[str] = exifdata.splitlines()
                except:
                    print("ERROR: Exif.readExif(",filename,"): error while reading!")
                    exifdataLines : list[str]= ['']
                # buid exif dict
                for each in exifdataLines:
                    tag,val = each.split(':',1)# tags and values are separated by a semi colon
                    exifDict[tag.strip()] = val.strip()
            else: print("ERROR: exiftool.exe not found!")

        else: print("ERROR: Exif.readExif(",filename,"): file not found!")

        return exifDict
        
        
    @staticmethod
    def recoverExifData(exif : dict[str, str]) -> dict[str, str]:
        """ filter raw dict to recover some data:
                color space
        """
        filteredExif : dict[str, str] = {}
        # colorSpace: 'Color Space', 'Profile Description', 'ColorSpace'
        exifColorSpace : list[str] = ['Color Space', 'Profile Description', 'ColorSpace']

        if exifColorSpace[0] in exif.keys():            filteredExif['Color Space'] = exif[exifColorSpace[0]]
        elif exifColorSpace[1] in exif.keys():          filteredExif['Color Space'] = exif[exifColorSpace[1]]
        elif exifColorSpace[2] in exif.keys():
            if exif[exifColorSpace[2]]==1:              filteredExif['Color Space'] =   'sRGB'
            elif exif[exifColorSpace[2]]==2:            filteredExif['Color Space'] =   'Adobe RGB (1998)'
        elif 'File Name' in exif.keys():
            filename : str = exif['File Name']
            if filename.endswith(('.hdr', '.HDR')):     filteredExif['Color Space'] =   'scRGB'
            elif filename.endswith(('.jpg','.JPG')):    filteredExif['Color Space'] =   'sRGB'

        # Bits Per Sample
        if 'Bits Per Sample' in exif.keys():            filteredExif['Bits Per Sample'] = exif['Bits Per Sample']
        elif 'File Name' in exif.keys():
            filename : str = exif['File Name']
            if filename.endswith(('.hdr', '.HDR')):     filteredExif['Bits Per Sample'] =   '32'
            elif filename.endswith(('.jpg','.JPG')):    filteredExif['Bits Per Sample'] =   '8'

        # Type
        if 'File Name' in exif.keys():
            filename : str = exif['File Name']
            if filename.endswith(('.hdr', '.HDR')):     filteredExif['Type'] =   'HDR'
            elif filename.endswith(('.jpg','.JPG')):    filteredExif['Type'] =   'SDR'

        # image width x height
        # Image Width                     : 1818
        # Image Height                    : 4000
        if 'Image Width' in exif.keys() and 'Image Height' in exif.keys():
           filteredExif['Size'] =   exif['Image Width']+' x '+exif['Image Height'] 

        return filteredExif





# ------------------ main -------------------------------
if __name__ == "__main__":
    path : str = "./imagesTest" ; filename : str = '01.jpg'
    #path : str = "C:/Users/rcozo/Dropbox/photos/samastro/hdr" ; filename : str = 'sadr.hdr'

    res : dict[str, str]|None= Exif.readExif(path, filename)
    print(res)

    if res:
        print(Exif.recoverExifData(res))