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
from typing import Tuple
from typing_extensions import Self
import os, json

# ------------------------------------------------------------------------------------------
# --- class Tags ---------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = False
# ------------------------------------------------------------------------------------------
class Tags:
    """manages user additional information, called Tags, defined by user; images tags are aggregated in a directory.  
        {
        'tagType 0': {'tagName 0 a': True|False, ..., 'tagName 0 n': True|False}, 
        ...
        'tagType K': {'tagName K a': True|False, ..., 'tagName K m': True|False}, 
        }"""
    # class attributes

    # constructor
    def __init__(self: Self, tags: dict[str, dict[str,bool]]) -> None:

        self.tags : dict[str, dict[str,bool]] = tags

    # methods
    ## load tags from file
    ## -------------------------------------------------------
    @staticmethod
    def load(imageDir: str, imageFilename: str, extraDir : str) -> Tags:
        # check if extra '.uHDR' dir exist
        extraPath = os.path.join(imageDir, extraDir) 
        if os.path.isdir(extraPath):
            tagsFilename= os.path.join(imageDir,extraDir,imageFilename[:-3]+'tags') 
            if os.path.exists(tagsFilename):
                with open(tagsFilename) as tagsfile:
                    tags :  Tags = Tags(json.load(tagsfile)) 
                    return tags
        return Tags({})

    ## save tags to file
    ## -------------------------------------------------------
    def save(self: Self, imageDir: str, extraDir: str, imageFilename : str) -> None:
        if debug : print(f'app.Tags.save({imageDir},{extraDir},{imageFilename})')
        # check if extra '.uHDR' dir exist
        extraPath = os.path.join(imageDir, extraDir) 
        if os.path.isdir(extraPath):
            tagsFilename= os.path.join(imageDir,extraDir,imageFilename[:-3]+'tags') 
            with open(tagsFilename,'w') as tagsfile:
                if debug : print(f'app.Tags.save({imageDir},{extraDir},{imageFilename}) > {self.tags}')
                json.dump(self.tags,tagsfile)       

    ## add
    ## -------------------------------------------------------
    def add(self: Self, type: str, name: str, value: bool) -> None:
        if debug : print(f'app.Tags.add({type},{name},{value})')

        if type in self.tags.keys():  self.tags[type][name] = value
        else: self.tags[type] = {name: value}

    def __repr__(self: Self) -> str: return str(self.tags)
    
    ## aggregate tags in a directory
    ## -------------------------------------------------------
    @staticmethod
    def aggregateTagsFiles(imagePath: str, extraPath: str) -> dict[str, dict[str,bool]]:
        """aggreagte image tags in a directory."""
        ePath: str = os.path.join(imagePath, extraPath) 
        allTags : list[ dict[str, dict[str,bool]]] = []

        if os.path.exists(ePath): 
            filenames = sorted(os.listdir(ePath))
            tagsFilenames = list(filter(lambda x: x.endswith('.tags'),filenames))

            for f in tagsFilenames:
                with open(os.path.join(ePath,f)) as tagsfile: 
                    tags : dict =  json.load(tagsfile)    
                    allTags.append(tags)
            
        return Tags.aggregateTagsData(allTags)

    ## -------------------------------------------------------
    @staticmethod
    def aggregateTagsData(tags: list[dict[str, dict[str,bool]]]) -> dict[str, dict[str,bool]]:
        """aggreagte image tags."""
        res : dict[str, dict[str,bool]] = {}

        for itags in tags:

                for tagType in itags.keys():
                    if not tagType in res: res[tagType] = {}
                    
                    for tagName in itags[tagType].keys():
                        res[tagType][tagName] = False
        return res    

    ## -------------------------------------------------------
    def toGUI(self:Self)-> dict[Tuple[str,str], bool]:
        """format tags (class Tags) to GUI 'tags'."""
        res = {}
        for tagType in sorted(self.tags.keys()):
            for tagName in sorted(self.tags[tagType].keys()):
                res[(tagType,tagName)] = self.tags[tagType][tagName]
        return res

    ## -------------------------------------------------------
    def aggregate(self: Self, other: Tags):
        """aggregate tags  with those of an other tags object."""

        for tagType in other.tags.keys():
            if not tagType in self.tags: self.tags[tagType] = {}
            for tagName in other.tags[tagType].keys():
                self.tags[tagType][tagName] = False
    ## -------------------------------------------------------
