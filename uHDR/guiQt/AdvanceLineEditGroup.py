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
from PyQt6.QtWidgets import QFormLayout, QWidget, QScrollArea
from PyQt6.QtCore import pyqtSignal, Qt

from guiQt.AdvanceFormLineEdit import AdvanceFormLineEdit

# ------------------------------------------------------------------------------------------
# --- AdvanceLineEditGroup(QWidget) --------------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = True
class AdvanceLineEditGroup(QScrollArea):
    # class attributes
    
    ## signal
    textChanged : pyqtSignal = pyqtSignal(tuple)

    def __init__(self : Self, dValues : dict[str, str|tuple[str, bool]]):
        
        super().__init__()

        # attributes
        self.active : bool = True
        # widgets
        self.lines : list[AdvanceFormLineEdit] =[]

        self.container : QWidget = QWidget()
        self.layout : QFormLayout = QFormLayout() ; self.container.setLayout(self.layout)

        for tag in dValues.keys():
            if type(dValues[tag]) == str:
                value  : str = dValues[tag] #type: ignore
                editable : bool = True
            else:
                value : str = dValues[tag][0]
                editable : bool = dValues[tag][1] #type: ignore
            line : AdvanceFormLineEdit= AdvanceFormLineEdit(tag,value, self.layout, editable)
            line.textChanged.connect(self.CBtextChanged)
            self.lines.append(line)

        # Scroll Area Properties
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.container) 

    # methods
    def setText(self: Self, texts : list[str]) -> None:
        assert len(texts) == len(self.lines)
        for i, text in enumerate(texts): self.lines[i].setText(text)

    ## callback        
    def CBtextChanged(self: Self, tag:str, value : str):
        if debug : print(f'AdvanceLineEditGroup.CBtextChanged({tag},{value})[{self.active}]')
        if self.active: 
            self.textChanged.emit((tag,value))
# ------------------------------------------------------------------------------


