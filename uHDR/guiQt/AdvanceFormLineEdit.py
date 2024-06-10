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
from PyQt6.QtWidgets import QFormLayout, QLabel, QLineEdit
from PyQt6.QtCore import pyqtSignal, QObject

# ------------------------------------------------------------------------------------------
# --- AdvanceFormLineEdit(QObject) ---------------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = False
class AdvanceFormLineEdit(QObject):
    # class attributes
    ## signal
    textChanged : pyqtSignal = pyqtSignal(str,str)

    # constructor
    def __init__(self: Self, labelName: str, defaultText: str, layout: QFormLayout, editable :bool = True) -> None:
        super().__init__()
        self.active : bool = True

        self.defaultText : str = defaultText
        self.editable : bool =  editable

        self.label : QLabel = QLabel(labelName)
        self.lineEdit : QLineEdit =QLineEdit(defaultText)
        if not self.editable : self.lineEdit.setReadOnly(True)
        
        self.lineEdit.editingFinished.connect(self.CBtextChanged)
        
        layout.addRow(self.label,self.lineEdit)

    # methods
    # --------------------------------------------------
    def CBtextChanged(self : Self) -> None:
        if debug : print(f'AdvanceFormLineEdit.CBtextChanged()')
        if self.active: self.textChanged.emit(self.label.text(), self.lineEdit.text())

    # --------------------------------------------------
    def setText(self : Self, txt : str) -> None: 
        if debug : print(f'AdvanceFormLineEdit.setText({txt})')
        if self.active:
            self.active = False
            self.lineEdit.setText(txt)
            self.active = True
        else:
            self.lineEdit.setText(txt)
# -------------------------------------------------------------------------------------------
