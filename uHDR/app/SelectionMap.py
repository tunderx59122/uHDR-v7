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

# ------------------------------------------------------------------------------------------
# --- class Score --------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = True
# ------------------------------------------------------------------------------------------
class SelectionMap:
    """user selection of images: by score, tags and name."""
    # constructor
    def __init__(self : SelectionMap, imageNames : list[str]):
        # attributes

        self.__imageNameToIsSelected : dict[str, bool] = {}
        self.__imageNameToGlobalIndex : dict[str, int] = {}

        self.__globalIndexToImageName : dict[int, str] = {}

        self.__globalIndexToSelectedIndex : dict[int, int|None] = {}   
        self.__selectedIndexToGlobalIndex : dict[int, int] = {}

        self.numberImages : int =0
        self.numberSelectedImages : int  =0  

        self.setImageNames(imageNames)
        
    # methods
    # ------------------------------------------------------------------------------------
    ## repr
    def __repr__(self: SelectionMap) -> str:
        res : str = '----------------- Selection map ------------------\n'
        for name, selected in self.__imageNameToIsSelected.items():
            res+= f'{name} : {selected} :: global:{self.__imageNameToGlobalIndex[name]} -> local: {self.__globalIndexToSelectedIndex[self.__imageNameToGlobalIndex[name]]} \n' 
        res += '--------------------------------------------------\n'
        res += f'number of selected image:{self.numberSelectedImages}/{self.numberImages}'+'\n'
        res += '--------------------------------------------------\n'

        return res

    ## ---------------------------------------------------------------------------------------
    ## reset dicts
    def reset(self: SelectionMap) -> None:
        """"set image filenames and select all."""  
        self.__imageNameToIsSelected  = {}
        self.__imageNameToGlobalIndex  = {}

        self.__globalIndexToImageName  = {}

        self.__globalIndexToSelectedIndex  = {}   
        self.__selectedIndexToGlobalIndex  = {}

        self.numberImages : int =0
        self.numberSelectedImages : int  =0 
    ## ---------------------------------------------------------------------------------------
    ## setImageNames: select all image
    def setImageNames(self: SelectionMap, names: list[str]) -> None:
        """"set image filenames and select all."""        
        
        self.reset()
        
        for i, name in enumerate(names):
            self.__imageNameToIsSelected[name] = True
            self.__imageNameToGlobalIndex[name] = i

            self.__globalIndexToImageName[i] = name

            self.__globalIndexToSelectedIndex[i] = i
            self.__selectedIndexToGlobalIndex[i] = i 

        self.numberImages= len(names)
        self.numberSelectedImages = self.numberImages

    ## ---------------------------------------------------------------------------------------
    ## selectAll
    def selectAll(self: SelectionMap) -> None:
        """select all images."""
        for i, name in enumerate(self.__imageNameToIsSelected.keys()):
                self.__imageNameToIsSelected[name] = True
                self.__imageNameToGlobalIndex[name] = i

                self.__globalIndexToImageName[i] = name

                self.__globalIndexToSelectedIndex[i] = i
                self.__selectedIndexToGlobalIndex[i] = i

        self.numberImages= len(self.__imageNameToIsSelected.keys())
        self.numberSelectedImages = self.numberImages
    # ---------------------------------------------------------------------------------------
    def applySelection(self: SelectionMap, selection: list[tuple[str,bool]]) -> None:
        """apply a selection."""
        
        self.__selectedIndexToGlobalIndex = {}

        sIdx  : int = 0
        self.numberSelectedImages = 0
        for gIdx, (name, selected) in enumerate(selection):
                self.__imageNameToIsSelected[name] = selected

                self.__imageNameToGlobalIndex[name] = gIdx

                self.__globalIndexToImageName[gIdx] = name

                if selected:
                    self.__globalIndexToSelectedIndex[gIdx] = sIdx
                    self.__selectedIndexToGlobalIndex[sIdx] = gIdx
                    sIdx = sIdx+1
                    self.numberSelectedImages +=1
                else:  
                    self.__globalIndexToSelectedIndex[gIdx] = None

        if debug: print(f'SelectionMap.applySelection({selection}):\n{self}')
    # ---------------------------------------------------------------------------------------
    def isSelected(self: SelectionMap, name : str) -> bool|None: 
        if name in self.__imageNameToIsSelected.keys() : return self.__imageNameToIsSelected[name]
        else:
            print(f'[ERROR] SelectionMap.isSelected({name}): imagefile "{name}" not found > return None')
            return None
    # ---------------------------------------------------------------------------------------
    def imageNameToGlobalIndex(self: SelectionMap, name : str)  -> int|None: 

        if name in self.__imageNameToGlobalIndex.keys() : return self.__imageNameToGlobalIndex[name]
        else:
            print(f'[ERROR] SelectionMap.imageNameToGlobalIndex({name}): imagefile "{name}" not found > return None')
            return None
    # ---------------------------------------------------------------------------------------
    def globalIndexToImageName(self: SelectionMap, gIdx: int) -> str|None :
        if gIdx in self.__globalIndexToImageName.keys(): return self.__globalIndexToImageName[gIdx]
        else:
            print(f'[ERROR] SelectionMap.globalIndexToImageName({gIdx}): key ({gIdx}) not found > return None')
            return None
    # ---------------------------------------------------------------------------------------
    def globalIndexToSelectedIndex(self : SelectionMap, gIdx :int) -> int|None: 
        if gIdx in self.__globalIndexToSelectedIndex.keys(): return self.__globalIndexToSelectedIndex[gIdx]
        else: return None
    # ---------------------------------------------------------------------------------------
    def selectedlIndexToGlobalIndex(self : SelectionMap, sIdx : int) -> int|None: 
        if sIdx in self.__selectedIndexToGlobalIndex.keys() : return self.__selectedIndexToGlobalIndex[sIdx]
        else: return None           
    # ---------------------------------------------------------------------------------------  
    def selectedIndexToImageName(self: SelectionMap, sIdx : int ) -> str|None:
        gIdx : int | None = self.selectedlIndexToGlobalIndex(sIdx)
        if gIdx != None: return self.globalIndexToImageName(gIdx)
        else: return None
    # ---------------------------------------------------------------------------------------
    def imageNameToSelectedIndex(self: SelectionMap, name : str) -> int|None:
        gIdx : int | None = self.imageNameToGlobalIndex(name)
        if gIdx != None : return self.globalIndexToSelectedIndex(gIdx)
        else : return None
    # ---------------------------------------------------------------------------------------
    def selectByScore(self : SelectionMap, scores :dict[str, int], scoresSelected : list[int]):
        """select images which score is in selected score."""

        imagesSelection : list[tuple[str,bool]] = []
        for name, score in scores.items():
            imagesSelection.append((name, score in scoresSelected))
        self.applySelection(imagesSelection)
    # ---------------------------------------------------------------------------------------
    def getSelectedImageNumber(self: SelectionMap) -> int : return self.numberSelectedImages
    # ---------------------------------------------------------------------------------------


        
            

