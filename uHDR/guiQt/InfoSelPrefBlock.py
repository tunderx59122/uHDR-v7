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
from typing import Tuple
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QTabWidget, QWidget
from PyQt6.QtGui import QDoubleValidator, QIntValidator 
from PyQt6.QtCore import Qt, pyqtSignal, QLocale


from guiQt.InfoScoreExifTags import InfoScoreExifTags
from guiQt.Selection import Selection
# ------------------------------------------------------------------------------------------
# --- class InfoSelPrefBlock (QTabWidget) --------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = True
# ------------------------------------------------------------------------------------------
class InfoSelPrefBlock(QTabWidget):
    # class attributes
    ## signal
    tagChanged : pyqtSignal = pyqtSignal(tuple,bool)
    scoreChanged : pyqtSignal = pyqtSignal(int)
    scoreSelectionChanged : pyqtSignal = pyqtSignal(list)
    # constructor
    def __init__(self:Self, tags : dict[Tuple[str,str], bool]) -> None:
        super().__init__()

        # attributes
        self.infoExifScoreTag : InfoScoreExifTags = InfoScoreExifTags(tags) 
        self.selection : Selection = Selection() 
        self.preferences : QWidget = QWidget() 

        # QTabWidget settup
        self.setTabPosition(QTabWidget.TabPosition.West)
        self.setMovable(True)

        # add widgets
        self.addTab(self.infoExifScoreTag,"Information")
        self.addTab(self.selection,"Selection")
        self.addTab(self.preferences,"Preferences")

        # callbacks
        self.infoExifScoreTag.tagChanged.connect(self.CBtagChanged)
        self.infoExifScoreTag.scoreChanged.connect(self.CBscoreChanged)

        self.selection.scoreSelectionChanged.connect(self.CBscoreSelectionChanged)
    
    # methods
    ## tags
    def setTags(self: Self, tags: dict[Tuple[str,str], bool]) -> None : 
        self.infoExifScoreTag.setTags(tags)

    def resetTags(self: Self) -> None:
        self.infoExifScoreTag.resetTags()
    
    ## score
    def setScore(self: Self, score:int) -> None:
        self.infoExifScoreTag.setScore(score)

    ## info
    def setInfo(self: Self, name:str, path:str, size : tuple[int,int] =(-1,-1), colorSpace : str = '...', type: str ='...', bps : int =-1) -> None:
        self.infoExifScoreTag.setInfo(name, path, size , colorSpace, type, bps )

    # -----------------------------------------------------------------
    def CBtagChanged(self, key: tuple[str, str], value : bool) -> None:
        if debug :print(f'guiQt.InfoSelPrefBlock.CBtagChanged({key},{value}) > emit !')
        self.tagChanged.emit(key,value)

    # -----------------------------------------------------------------
    def CBscoreChanged(self, value : int) -> None:
        if debug :print(f'guiQt.InfoSelPrefBlock.CBscoreChanged({value}) > emit !')
        self.scoreChanged.emit(value)


    # ---------------------------------------------------------------
    def CBscoreSelectionChanged(self: Self, scoreSelection: list) -> None:
        if debug : print(f'guiQt.InfoSelPrefBlock.CBscoreSelectionChanged({scoreSelection})') 
        self.scoreSelectionChanged.emit(scoreSelection)
# ------------------------------------------------------------------------------------------


        