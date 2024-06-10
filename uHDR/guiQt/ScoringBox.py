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
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QCheckBox, QFrame
from PyQt6.QtCore import pyqtSignal, QObject
from functools import partial
# -------------------------------------------------------------------------------------------
# --- ScoringBox (QFrame) -------------------------------------------------------------------
# -------------------------------------------------------------------------------------------

class ScoringBox(QFrame):
    # class attributes
    ## signal
    scoreChanged : pyqtSignal = pyqtSignal(int)

    # constructor
    def __init__(self: Self, name: str, scoreRange : int = 5):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)

        self.active : bool = True
        self.name :  str = name
        self.scoreRange : int = scoreRange
        self.score : int = 0

        # widget
        self.topLayout : QHBoxLayout = QHBoxLayout()
        self.setLayout(self.topLayout)

        self.label : QLabel = QLabel(self.name)
        self.topLayout.addWidget(self.label)
        self.topLayout.addStretch()

        self.checkBoxes : list[QCheckBox] = []
        for i in range(self.scoreRange):
            # if i == 0:
            #     pass
            #     cb : QCheckBox = QCheckBox("_")
            # else:
            #     cb : QCheckBox = QCheckBox(str(i))
            cb : QCheckBox = QCheckBox(str(i))
            self.checkBoxes.append(cb)
            self.topLayout.addWidget(cb)
            cb.toggled.connect(partial(self.CBscoreChanged,i))

        self.updateScore()

    # methods
    def updateScore(self: Self) -> None:
        self.active = False
        for i, cb in enumerate(self.checkBoxes): cb.setChecked(i <= self.score)
        self.active = True

    def setScore(self:Self, score :int) -> None:
        self.score = score
        self.updateScore()
        
    
    ## callbacks
    def CBscoreChanged(self:Self, score:int) -> None :
        if self.active:
            self.score  = score
            self.updateScore()
            self.scoreChanged.emit(self.score)
    
# -------------------------------------------------------------------------------------------
