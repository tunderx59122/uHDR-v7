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
from PyQt6.QtWidgets import QFormLayout, QLabel, QCheckBox
from PyQt6.QtCore import pyqtSignal, QObject


# ------------------------------------------------------------------------------------------
# --- AdvanceFormCheckBox(QObject) ---------------------------------------------------------
# ------------------------------------------------------------------------------------------
debug = False
class AdvanceFormCheckBox(QObject) :

    toggled : pyqtSignal = pyqtSignal(tuple,bool)

    def __init__(self: Self, leftText: str, rightText: str, layout: QFormLayout, checked: bool = False, editable : bool = True) -> None:
        super().__init__()

        # attributes
        self.keys : tuple[str, str] = (leftText, rightText)
        self.checked : bool = checked

        self.active : bool = True
        self.editable : bool = editable
        self.label = QLabel(leftText)
        self.checkbox =QCheckBox(rightText)
        self.checkbox.setChecked(checked)
        layout.addRow(self.label,self.checkbox)

        self.checkbox.toggled.connect(self.CBtoggled)

    # methods
    def getKeys(self: Self) -> tuple[str,str]:
        return self.keys      

    def setChecked(self: Self, checked:bool) :
        if self.active:
            self.active = False
            self.checkbox.setChecked(checked)
            self.active = True
        else:
            self.checkbox.setChecked(checked)

    ## callbacks
    def CBtoggled(self: Self) -> None:
        """"callback called when checkbox is toggled.""" 
        if debug : print(f'AdvanceFormCheckBox.CBtoggled() > {(self.label.text(), self.checkbox.text()), self.checkbox.isChecked()} ')
        if self.editable:
            if self.active:
                if debug : print(f'AdvanceFormCheckBox.CBtoggled() > emit > {(self.label.text(), self.checkbox.text()), self.checkbox.isChecked()} ')
                self.toggled.emit((self.label.text(), self.checkbox.text()), self.checkbox.isChecked()) 
        else:
            self.checkbox.setChecked(self.checked)  
