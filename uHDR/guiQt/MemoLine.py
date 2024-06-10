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
import sys
from typing_extensions import Self
from PyQt6.QtWidgets import QFrame, QPushButton, QCheckBox, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QLocale

# ------------------------------------------------------------------------------------------
# --- class MemoLine(QFrame) ---------------------------------------------------------------
# ------------------------------------------------------------------------------------------
class MemoLine(QFrame):
    # static attributes
    ## signal
    setClicked : pyqtSignal = pyqtSignal(str)
    activateClicked : pyqtSignal = pyqtSignal(str)
    resetClicked : pyqtSignal = pyqtSignal(str)

    
    # constructor
    def __init__(self:Self, name : str, activated :bool = False) -> None:
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)

        # attributes
        self.active : bool = True

        self.name : str = name
        self.mem :bool = False
        self.activated : bool = activated

        # widgets
        self.topLayout : QHBoxLayout = QHBoxLayout()
        self.setLayout(self.topLayout)

        self.label : QLabel = QLabel(self.name)
        self.setButton : QPushButton = QPushButton('set')
        self.activateButton : QPushButton = QPushButton('activate')
        self.resetButton : QPushButton = QPushButton('reset')
        self.activatedCheckBox : QCheckBox = QCheckBox('')
        self.updateMessage()
        self.activatedCheckBox.setChecked(self.activated)

        # addWidget to Layout
        self.topLayout.addWidget(self.label)
        self.topLayout.addWidget(self.setButton)
        self.topLayout.addWidget(self.activateButton)
        self.topLayout.addWidget(self.resetButton)
        self.topLayout.addWidget(self.activatedCheckBox)

        # callbacks
        self.activateButton.clicked.connect(self.CBactivate)
        self.activatedCheckBox.toggled.connect(self.CBactivatedCheckBox)
        self.resetButton.clicked.connect(self.CBreset)
        self.setButton.clicked.connect(self.CBset)

    # methods
    ## callbacks
    def CBactivatedCheckBox(self: Self) -> None: 
        self.activatedCheckBox.setChecked(self.activated)
        self.updateMessage()

    def CBactivate(self : Self) -> None:
        if self.mem:
            self.activated = not self.activated
            self.activatedCheckBox.setChecked(self.activated)
        self.updateMessage()

    def CBreset(self : Self) -> None:
        self.activated = False
        self.activatedCheckBox.setChecked(self.activated)  
        self.mem = False 
        self.updateMessage() 

    def CBset(self: Self) -> None:
        self.mem = True
        self.updateMessage()
  
    # update message
    def updateMessage(self: Self):
        if self.mem :
            if self.activated:
                self.activatedCheckBox.setText(self.name +' is active')
            else:
                self.activatedCheckBox.setText(self.name +' is ready')
        else:
            self.activatedCheckBox.setText(self.name +' is empty')

# --------------------------------------------------------------------------------------





