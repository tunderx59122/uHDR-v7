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
import copy
from typing_extensions import Self
from xmlrpc.client import boolean
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout,QPushButton, QLabel, QLineEdit, QSlider, QCheckBox
from PyQt6.QtGui import QDoubleValidator, QIntValidator 
from PyQt6.QtCore import Qt, pyqtSignal, QLocale

# ------------------------------------------------------------------------------------------
# --- class AdvanceSliderLine(QFrame) ------------------------------------------------------
# ------------------------------------------------------------------------------------------
class AdvanceSliderLine(QFrame):
    # static attributes
    valueChanged : pyqtSignal = pyqtSignal(str,float)

    # consructor
    def __init__(self: Self, name:str, default: float, range: tuple[int,int],rangeData : tuple[float, float] | None= None,nameLength : int = 10, precision : int =100) -> None:
        super().__init__()

        # attributes

        self.name : str = name
        self.active : bool = True
        self.default : float = default

        self.guiRange : tuple[int,int] = range
        self.dataRange : tuple[float, float] = rangeData if rangeData else copy.deepcopy(range)


        self.precision : int = precision

        ## widgets

        self.hbox = QHBoxLayout()
        self.setLayout(self.hbox)

        # label, slider, lineEdit, reset
        name = name if len(name)>= nameLength else ' '*((nameLength-len(name))//2)+name+' '*((nameLength-len(name))//2)
        self.label : QLabel= QLabel(name)
        self.slider : QSlider= QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(*range)
        self.slider.setValue(int(default))
        self.edit : QLineEdit= QLineEdit()
        self.edit.setText(str(round(default*self.precision)/self.precision))

        validator : QDoubleValidator= QDoubleValidator()
        locale : QLocale = QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)
        validator.setLocale(locale)
        self.edit.setValidator(validator)      

        self.reset : QPushButton= QPushButton("reset")

        self.hbox.addWidget(self.label,20)
        self.hbox.addWidget(self.slider,50)
        self.hbox.addWidget(self.edit,10)
        self.hbox.addWidget(self.reset,10)

        # callbacks
        self.slider.valueChanged.connect(self.CBsliderChanged)
        self.edit.editingFinished.connect(self.CBeditChanged)
        self.reset.clicked.connect(self.CBreset)

    # methods
    def setValue(self: Self, val: float) -> None:
        self.active = False
        self.slider.setValue(self.toGui(val))
        self.edit.setText(str(round(val*self.precision)/self.precision))
        self.active = True

    def toGui(self, data: float) -> int:
        u : float = (data - self.dataRange[0])/(self.dataRange[1] -self.dataRange[0])
        guiValue : float = self.guiRange[0]*(1-u)+self.guiRange[1]*u
        return int(guiValue)


    def toValue(self, data:int) -> float:
        u : float = (data - self.guiRange[0])/(self.guiRange[1] -self.guiRange[0])
        value : float = self.dataRange[0]*(1-u)+self.dataRange[1]*u
        return value

    # callbacks
    def CBsliderChanged(self : Self) -> None:
        if self.active:
            val : float = round(self.toValue(self.slider.value())*self.precision)/self.precision
            self.setValue(val)
            self.valueChanged.emit(self.name, val)

    def CBeditChanged(self: Self) -> None:
        if self.active:
            val : float = round(float(self.edit.text())*self.precision)/self.precision
            self.setValue(val)
            self.valueChanged.emit(self.name, val)

    def CBreset(self: Self) -> None:
        if self.active:
            self.setValue(self.default)
            self.valueChanged.emit(self.name, int(self.default))
# -------------------------------------------------------------------------------------------
