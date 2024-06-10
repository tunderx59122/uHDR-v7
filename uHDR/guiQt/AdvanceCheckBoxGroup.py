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
from PyQt6.QtWidgets import QFormLayout, QWidget, QScrollArea, QLayout
from PyQt6.QtCore import pyqtSignal, Qt

from guiQt.AdvanceFormCheckBox import AdvanceFormCheckBox

# ------------------------------------------------------------------------------------------
# --- AdvanceLineEditGroup(QWidget) --------------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = False
class AdvanceCheckBoxGroup(QScrollArea):
    # class attributes
    pass
    ## signal
    toggled : pyqtSignal = pyqtSignal(tuple,bool)

    def __init__(self : Self, dValues : dict[tuple[str,str], bool| tuple[bool, bool]]):
        
        super().__init__()
        self.lines : list[AdvanceFormCheckBox] =[]

        self.container : QWidget = QWidget()
        self.layout : QFormLayout = QFormLayout() ; self.container.setLayout(self.layout)
        self.layout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)


        checked :bool = False
        editable :bool =  True
        for key in dValues.keys():
            if type(dValues[key]) == bool :
                checked  = dValues[key]     #type: ignore
                editable = True
            elif len(dValues[key]) == 2:    #type: ignore
                checked  = dValues[key][0]  #type: ignore
                editable = dValues[key][1]  #type: ignore

            line : AdvanceFormCheckBox= AdvanceFormCheckBox(key[0] ,key[1], self.layout, checked =checked, editable= editable)
            #line.toggled.connect(self.CBtextChanged)
            line.toggled.connect(self.CBtoggled)
            self.lines.append(line)

        # Scroll Area Properties
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.container) 

 

    # methods
    ## getByKey
    def getByKey(self : Self, key : tuple[str,str]) -> AdvanceFormCheckBox | None:
        res : AdvanceFormCheckBox | None = None
        for line in self.lines:
            if line.getKeys() == key :
                res=line ; break
        return res

    ## setValues
    def setValues(self: Self, values : dict[tuple[str,str], bool]) -> None :
        for key in values.keys():
            advanceFormCheckBox : AdvanceFormCheckBox | None = self.getByKey(key)
            if advanceFormCheckBox:  
                advanceFormCheckBox.setChecked(values[key])
                if debug : print(f'AdvanceCheckBoxGroup.setValues(..) > setValue() > {key} -> {values[key]}')

    ## resetValues
    def resetValues(self: Self) -> None:
        for line in self.lines: line.setChecked(False)

    ## add line
    def addLine(self: Self, dValues : dict[tuple[str,str], bool| tuple[bool, bool]]) -> None:
        checked :bool = False
        editable :bool =  True
        for key in dValues.keys():
            if type(dValues[key]) == bool :
                checked  = dValues[key]     #type: ignore
                editable = True
            elif len(dValues[key]) == 2:    #type: ignore
                checked  = dValues[key][0]  #type: ignore
                editable = dValues[key][1]  #type: ignore

            line : AdvanceFormCheckBox= AdvanceFormCheckBox(key[0] ,key[1], self.layout, checked =checked, editable= editable)
            line.toggled.connect(self.CBtoggled)
            self.lines.append(line)
    ## remove line
    def removeLine(self: Self, keys : tuple[str, str]) -> None:
        if debug : print(f'AdvanceCheckBoxGroup.removeLine({keys}):')
        for i, line in enumerate(self.lines):
            if line.keys == keys:
                self.layout.removeRow(i)
    ## removeAll
    def removeAll(self: Self) -> None:
        for i in range(self.layout.rowCount()):
            if debug : print(f'self.layout.rowCount():{self.layout.rowCount()}')
            self.layout.removeRow(0)
        self.lines = []

    # callbacks        
    def CBtextChanged(self: Self, tag:tuple[str,str], value : bool):
        if debug : print(f'AdvanceCheckBoxGroup.CBtextChanged()-> signal({tag[0]}::{tag[1]},{value})')

    def CBtoggled(self: Self, key: tuple[str,str], toggled_: bool)  -> None:
        if debug : print(f'AdvanceCheckBoxGroup.CBtoggled({key},{toggled_}) > emit !')
        self.toggled.emit(key, toggled_)

