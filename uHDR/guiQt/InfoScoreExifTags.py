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
from PyQt6.QtWidgets import QVBoxLayout, QFrame, QLayout
from PyQt6.QtCore import pyqtSignal

from guiQt.InfoBase import InfoBase
from guiQt.ScoringBox import ScoringBox
from guiQt.Tags import Tags

# -------------------------------------------------------------------------------------------
# --- InfoBase (QFrame) ---------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
debug : bool = False
# ------------------------------------------------------------------------------------------
class InfoScoreExifTags(QFrame):
    # class attributes
    ## signal
    tagChanged : pyqtSignal = pyqtSignal(tuple,bool)
    scoreChanged : pyqtSignal =pyqtSignal(int)
    # constructor
    def __init__(self: Self, itags: dict[Tuple[str,str], bool]) -> None:
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)  

        # attributes

        ## widgets
        self.infoBase :  InfoBase = InfoBase()
        self.score : ScoringBox = ScoringBox('score:', 6)

        self.tags : Tags = Tags(itags)

        ## layout
        self.topLayout : QVBoxLayout = QVBoxLayout()
        self.setLayout(self.topLayout)
        self.topLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

        ## add widgets to layout
        self.topLayout.addWidget(self.infoBase)
        self.topLayout.addWidget(self.score)
        self.topLayout.addWidget(self.tags)
        self.topLayout.addStretch()


        # callbacks
        self.tags.tagChanged.connect(self.CBtagChanged)
        self.score.scoreChanged.connect(self.CBscoreChanged)

    # methods
    ## tags
    def setTags(self: Self, tags: dict[Tuple[str,str], bool]) -> None: 
        self.tags.setTags(tags)

    def resetTags(self: Self) -> None:
        self.tags.resetTags()

    ## info
    def setInfo(self: Self, name: str, path: str, size : tuple[int,int] =(-1,-1), colorSpace : str = '...', type: str ='...', bps : int =-1) -> None:
        self.infoBase.setInfo(name,path, size, colorSpace, type, bps)


    ## score
    def setScore(self: Self, score :int ) -> None:
        self.score.setScore(score)

    # -----------------------------------------------------------------
    def CBtagChanged(self, key: tuple[str, str], value : bool) -> None:
        if debug : print(f'guiQt.InfoScoreExifTags.CBtagChanged({key},{value}) > emit !')
        self.tagChanged.emit(key,value)
    # -----------------------------------------------------------------
    def CBscoreChanged(self, value :int) -> None:
        if debug : print(f'guiQt.InfoScoreExifTags.CBscoreChanged({value}) > emit !')
        self.scoreChanged.emit(value)