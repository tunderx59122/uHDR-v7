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
import json, os

from app.Tags import Tags
# ------------------------------------------------------------------------------------------
# ---- class Prefs -------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

class Prefs:
    # class attributes
    # default values: updated when Prefs.load() is called
    prefsFile : str = './preferences/prefs.json'    
    currentDir : str = '.'                          
    imgExt : list[str] = ['.jpg','.hdr']
    HDRdisplay : str = 'none'
    HDRdisplays : dict = {}
    extraPath : str = '.uHDR'
    thumbnailPrefix : str = "_"
    thumbnailMaxSize : int = 800

    tags : dict[str, dict[str,bool]] = {}

    gallerySize : tuple[int,int] = (2,2)

    #

    # constructor
    def __init__(self: Self) -> None: pass

    # methods



    # static methods
    @staticmethod
    def load() -> None:
        with open('./preferences/prefs.json') as f: 
            allPrefs : dict =  json.load(f)
            if "imagePath" in allPrefs.keys(): Prefs.currentDir = allPrefs["imagePath"]
            if "extraPath" in allPrefs.keys(): Prefs.extraPath = allPrefs["extraPath"]
            if "HDRdisplay" in allPrefs.keys(): Prefs.HDRdisplay = allPrefs["HDRdisplay"]
            if "HDRdisplays" in allPrefs.keys(): Prefs.HDRdisplays = allPrefs["HDRdisplays"]
            if "imgExt" in allPrefs.keys(): Prefs.imgExt = allPrefs["imgExt"]
            if "thumbnailPrefix" in allPrefs.keys(): Prefs.thumbnailPrefix = allPrefs["thumbnailPrefix"]
            if "thumbnailMaxSize" in allPrefs.keys(): Prefs.thumbnailMaxSize = allPrefs["thumbnailMaxSize"]

            # tags
            if "tags" in allPrefs.keys():
                listFileTags : list[str] = allPrefs["tags"]

                allTags : list[ dict[str, dict[str,bool]]] = []

                for tagFile in listFileTags:

                    with open(os.path.join('./preferences/',tagFile)) as f: 
                            tags : dict =  json.load(f)    
                            allTags.append(tags)
                    
                Prefs.tags =  Tags.aggregateTagsData(allTags)

            # gui
            if "gui" in allPrefs.keys():
                if "gallerySize" in allPrefs["gui"].keys(): Prefs.gallerySize = tuple(allPrefs["gui"]["gallerySize"])

    @staticmethod
    def __str__() -> str:
        res : str = ''
        res+= f'preferences file: {Prefs.prefsFile}' + '\n'
        res+= f'working directory: {Prefs.currentDir}' + '\n'
        res+= f'extra directory: {Prefs.extraPath}' + '\n'
        res += f'thumbnail prefixe: {Prefs.thumbnailPrefix}' + '\n'
        res += f'output HDR display: {Prefs.HDRdisplay}' + '\n'
        res += 'supported HDR displays:' +'\n'
        for display in Prefs.HDRdisplays.keys():
            res+= f'\t {display}: {Prefs.HDRdisplays[display]}'+'\n'
        res += 'supported image format:'+'\n'
        for ext in Prefs.imgExt:
            res+= f'\t {ext} \n'

        res +=f'gallery size: {Prefs.gallerySize}'

        res += f'tags: {Prefs.tags}'
        return res


