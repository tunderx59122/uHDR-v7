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
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout,QPushButton, QLabel, QLineEdit, QSlider, QCheckBox
from PyQt6.QtGui import QDoubleValidator 
from PyQt6.QtCore import Qt, pyqtSignal, QLocale

# ------------------------------------------------------------------------------------------
# --- class AdvanceSlider(QFrame) ------------------------------------------------------
# ------------------------------------------------------------------------------------------
class AdvanceSlider(QFrame):
    valueChanged : pyqtSignal = pyqtSignal(float,bool)
    autoClicked : pyqtSignal = pyqtSignal()
    activeToggled : pyqtSignal = pyqtSignal(bool)

    def __init__(self: Self, name: str,defaultValue : float, rangeGUI: tuple[int,int], rangeData : tuple[float, float] | None= None, precision = 1000) -> None:
        super().__init__()

        self.active  : bool = True
        self.guiRange : tuple[int, int]= (rangeGUI)
        self.dataRange : tuple[float, float]= rangeData if rangeData else (float(self.guiRange[0]), float(self.guiRange[1]))
        self.defaultValue : float= defaultValue
        self.precision : int = precision

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.firstrow : QFrame = QFrame()

        self.vbox : QVBoxLayout = QVBoxLayout()
        self.hboxTop : QHBoxLayout= QHBoxLayout()
        self.hbox : QHBoxLayout= QHBoxLayout()
        
        self.firstrow.setLayout(self.hbox)

        self.checkBoxActive : QCheckBox = QCheckBox("active")
        self.checkBoxActive.setChecked(True)

        self.label : QLabel = QLabel(name)
        self.auto : QPushButton= QPushButton("auto")
        self.editValue : QLineEdit = QLineEdit()
        validator : QDoubleValidator= QDoubleValidator()
        locale : QLocale = QLocale(QLocale.Language.English, QLocale.Country.UnitedStates)
        validator.setLocale(locale)

        self.editValue.setValidator(validator)

        self.editValue.setText(str(self.defaultValue))
        self.reset : QPushButton= QPushButton("reset")

        self.hbox.addWidget(self.label)
        self.hbox.addWidget(self.auto)
        self.hbox.addWidget(self.editValue)
        self.hbox.addWidget(self.reset)
        self.hbox.addWidget(self.checkBoxActive)

        self.slider : QSlider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(self.guiRange[0],self.guiRange[1])
        self.slider.setValue(self.toGui(self.defaultValue))
        self.slider.setSingleStep(1) 

        self.vbox.addWidget(self.firstrow)
        self.vbox.addWidget(self.slider)

        self.setLayout(self.vbox)

        # connection to signal: slider/reset/auto
        self.slider.valueChanged.connect(self.sliderChanged)
        self.editValue.editingFinished.connect(self.valueEdited)
        self.reset.clicked.connect(self.resetClicked)
        self.auto.clicked.connect(self.autoClickedCB)
        self.checkBoxActive.toggled.connect(self.activeChanged)
    
    # methods
    # -------------------------------------------------- 
    def toGui(self, data: float) -> int:
        u : float = (data - self.dataRange[0])/(self.dataRange[1] -self.dataRange[0])
        guiValue : float = self.guiRange[0]*(1-u)+self.guiRange[1]*u
        return int(guiValue)
    # -------------------------------------------------- 
    def toValue(self, data:int) -> float:
        u : float = (data - self.guiRange[0])/(self.guiRange[1] -self.guiRange[0])
        value : float = self.dataRange[0]*(1-u)+self.dataRange[1]*u
        return value
    # callBack
    # -------------------------------------------------- 
    def activeChanged(self): 
        self.activeToggled.emit(self.checkBoxActive.isChecked())
    # -------------------------------------------------- 
    def sliderChanged(self: Self): 

        guiData : int = self.slider.value()
        value : float = round(self.toValue(guiData)*self.precision)/self.precision
        if self.active :
            self.active = False
            self.editValue.setText(str(value))
            self.active = True
            self.valueChanged.emit(value,self.checkBoxActive.isChecked())
        else:
            self.editValue.setText(str(value))
    # -------------------------------------------------
    def valueEdited(self : Self) -> None:
        value : float = round(float(self.editValue.text())*self.precision)/self.precision
        if self.active:
            self.active = False
            self.editValue.setText(str(value))
            self.slider.setValue(self.toGui(value))
            self.active = True
            self.valueChanged.emit(value,self.checkBoxActive.isChecked())
        else:
            self.slider.setValue(self.toGui(value))
    # -------------------------------------------------
    def resetClicked(self: Self) -> None:
        if self.active:
            self.active = False
            self.editValue.setText(str(self.defaultValue))
            self.slider.setValue(self.toGui(self.defaultValue))
            self.active = True
            self.valueChanged.emit(self.defaultValue,self.checkBoxActive.isChecked())
        else:
            self.editValue.setText(str(self.defaultValue))
            self.slider.setValue(self.toGui(self.defaultValue))
    # -------------------------------------------------
    def autoClickedCB(self: Self) -> None:
        self.autoClicked.emit()

# -------------------------------------------------------------------------------------------

