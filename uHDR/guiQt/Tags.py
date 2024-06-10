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
from PyQt6.QtWidgets import QFormLayout, QWidget, QScrollArea, QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtWidgets import QLayout
from PyQt6.QtCore import pyqtSignal, Qt

from guiQt.AdvanceCheckBoxGroup import AdvanceCheckBoxGroup
from guiQt.AdvanceLineEditGroup import AdvanceLineEditGroup

# ------------------------------------------------------------------------------------------
# --- AdvanceLineEditGroup(QFrame) ---------------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = False
# ------------------------------------------------------------------------------------------
class Tags (QFrame):
    # class attributes
    ## signal
    tagChanged : pyqtSignal = pyqtSignal(tuple,bool)

    # constructor
    def __init__(self : Self, tags : dict[tuple[str,str], bool]) -> None:
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)

        # attributes
        self.tags : dict[tuple[str,str], bool] = tags
        # store new tag (type, name)
        self.newTag : tuple[str, str] = ('','')

        # layout, widgets
        self.topLayout : QVBoxLayout = QVBoxLayout()
        self.setLayout(self.topLayout)
        self.topLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinAndMaxSize)

        self.tagsGroup : AdvanceCheckBoxGroup = AdvanceCheckBoxGroup(self.tags) #type: ignore
        self.topLayout.addWidget(self.tagsGroup)

        self.tagsGroup.setMinimumHeight(400)

        # edit tags
        self.label : QLabel =QLabel('add tag(type, name):')
        self.tagTypeName : AdvanceLineEditGroup = AdvanceLineEditGroup({'type':'', 'name': ''})
        self.ok : QPushButton = QPushButton(' ok ')

        self.topLayout.addWidget(self.label)
        self.topLayout.addWidget(self.tagTypeName)
        self.topLayout.addWidget(self.ok)

        ## callbacks
        self.tagsGroup.toggled.connect(self.CBtagChanged)
        self.tagTypeName.textChanged.connect(self.CBnewtag)
        self.ok.clicked.connect(self.CBaddTag)

    # methods
    def newTags(self: Self) -> None : 
        newType : str = self.newTag[0]
        newName : str = self.newTag[1]
        if (newType  != '') and (newName != ''):
            # no empty field
            if not ((newType, newName) in self.tags.keys()):
                if debug : print(f'guiQt.Tags.checkTags() > adding tag:   {newType},{newName}')
                self.tags[(newType,newName)] =  False
                self.tagsGroup.addLine({(newType,newName):False}) #type: ignore
                self.tagChanged.emit((newType,newName),False)


            else:
                print(f"ERROR in new tag: ({newType},{newName}) alreday in tags")
                pass
        else:
            print("ERROR in new tag: type nor name could be ''")
            pass
    
    # -----------------------------------------------------------------

    def setTags(self: Self, tags :dict[tuple[str,str], bool]) -> None: 
        if debug : print(f'guiQt.Tags.setTags({tags})')
        self.tagsGroup.setValues(tags)

    def resetTags(self: Self) -> None:
        self.tagsGroup.resetValues()

    # -----------------------------------------------------------------
    ## callbacks
    def CBnewtag(self: Self, kv):
        if kv[0] == 'type':
            self.newTag= (kv[1], self.newTag[1])
        elif kv[0] == 'name':
            self.newTag = (self.newTag[0],kv[1])
    # ------------------------------------------------------------------
        
    def CBaddTag(self: Self) -> None:
        self.newTags()
        self.tagTypeName.setText(['',''])
        self.newTag = ('','')

    # -----------------------------------------------------------------
    def CBtagChanged(self, key: tuple[str, str], value : bool) -> None:
        if debug : print(f'guiQt.Tags.CBtagChanged({key},{value}) > emit !')
        self.tagChanged.emit(key,value)




