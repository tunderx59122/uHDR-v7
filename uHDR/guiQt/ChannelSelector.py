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
import numpy as np, copy
from typing_extensions import Self
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIntValidator

from guiQt.ImageWidget import ImageWidget

# ------------------------------------------------------------------------------------------
class ChannelSelector(QFrame):
    # class attributes
    ## signal
    valuesChanged : pyqtSignal = pyqtSignal(str,int, int)
    def __init__(self : Self, name : str, colourDataRGB : np.ndarray, range :tuple[int,int], default : tuple[int,int]  ) -> None:
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)

        # attributes
        self.name : str = name
        self.default : tuple[int,int] = default
        self.values : tuple[int,int] = copy.deepcopy(default)
        self.active : bool = True

        # layout
        self.vbox : QVBoxLayout= QVBoxLayout()
        self.setLayout(self.vbox)
        # container, layout: label and values
        self.labelValues : QFrame = QFrame()
        self.hbox : QHBoxLayout = QHBoxLayout()
        self.labelValues.setLayout(self.hbox)
        self.labelSelector = QLabel(name)

        self.label : QLabel =QLabel(name)
        self.min : QLineEdit = QLineEdit()
        self.min.setValidator(QIntValidator())
        self.min.setText(str(default[0]))

        self.max : QLineEdit = QLineEdit()
        self.min.setValidator(QIntValidator())
        self.max.setText(str(default[1]))

        self.reset : QPushButton = QPushButton('reset')

        self.hbox.addWidget(self.label)
        self.hbox.addStretch()
        self.hbox.addWidget(QLabel('min:'))
        self.hbox.addWidget(self.min)
        self.hbox.addWidget(QLabel('max:'))
        self.hbox.addWidget(self.max)
        self.hbox.addStretch()
        self.hbox.addWidget(self.reset)

        # image
        self.imageWidget : ImageWidget = ImageWidget()
        self.imageWidget.setMinimumSize(2, 22) #2,72
        self.imageWidget.setPixmap(colourDataRGB)
        
        # slider min
        self.sliderMin = QSlider(Qt.Orientation.Horizontal)
        self.sliderMin.setRange(*range)
        self.sliderMin.setValue(default[0])
        self.sliderMin.setSingleStep(1)
        # slider max
        self.sliderMax = QSlider(Qt.Orientation.Horizontal)
        self.sliderMax.setRange(*range)
        self.sliderMax.setValue(default[1])
        self.sliderMax.setSingleStep(1)

        # add to layout
        self.vbox.addWidget(self.labelValues)
        self.vbox.addWidget(self.imageWidget)
        self.vbox.addWidget(self.sliderMin)
        self.vbox.addWidget(self.sliderMax)

        ## callbacks
        self.sliderMin.valueChanged.connect(self.CBsliderMin)
        self.sliderMax.valueChanged.connect(self.CBsliderMax)
        self.min.editingFinished.connect(self.CBminEdited)
        self.max.editingFinished.connect(self.CBmaxEdited)
        self.reset.clicked.connect(self.CBreset)

    # methods
    def sliderValues(self:Self) -> tuple[int,int]:
        min : int = self.sliderMin.value()
        max :int = self.sliderMax.value()
        return (min, max)

    # setValues
    def setValues(self : Self, min :int,max:int) -> None:
        self.active = False
        if min > max:
            temp : int = temp
            min = max ; max = temp
        self.values = (min,max)
        self.sliderMin.setValue(min)
        self.sliderMax.setValue(max)
        self.min.setText(str(min))
        self.max.setText(str(max))

        self.active = True

    # getValues
    def getValues(self:Self) -> tuple[int, int]: return self.sliderValues()

    ## callbacks
    def CBreset(self : Self) -> None :
        self.values = copy.deepcopy(self.default)
        self.setValues(*self.values)
        self.valuesChanged.emit(self.name,*self.values)

    def CBsliderMin(self:Self) -> None:
        if self.active: 
            min, max = self.sliderValues()
            min = min if min<= max else max
            self.values = (min,max)
            self.setValues(min,max)
            self.valuesChanged.emit(self.name,*self.values)

    def CBsliderMax(self:Self) -> None:
        if self.active :
            min, max = self.sliderValues()
            max = max if min<= max else min
            self.values = (min,max)
            self.setValues(min,max)
            self.valuesChanged.emit(self.name,*self.values)

    def CBminEdited(self : Self) -> None :
        if self.active :
            min : int = int(self.min.text())
            min = min if min<= self.values[1] else self.values[1]
            self.values = (min,self.values[1])
            self.setValues(*self.values) 
            self.valuesChanged.emit(self.name,*self.values)

    def CBmaxEdited(self : Self) -> None :
        if self.active :
            max : int = int(self.max.text())
            max = max if self.values[0] <= max else self.values[0]
            self.values = (self.values[0],max)
            self.setValues(*self.values)        
            self.valuesChanged.emit(self.name,*self.values)
# -------------------------------------------------------------------------

