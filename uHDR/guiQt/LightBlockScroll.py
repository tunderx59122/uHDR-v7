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
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal

from guiQt.LightBlock import LightBlock


# ------------------------------------------------------------------------------------------
# --- class LightBlockScroll (QScrollArea) -------------------------------------------------
# ------------------------------------------------------------------------------------------
class LightBlockScroll(QScrollArea):
    # class attributes
    ## signal
    imageSelected = pyqtSignal(object)
    # constructor
    def __init__(self : Self) -> None:
        super().__init__()


        ## lightblock widget
        self.light : LightBlock = LightBlock()
        self.light.setMinimumSize(500,1500)

        

        ## Scroll Area Properties
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True) 

        self.setWidget(self.light)
# ------------------------------------------------------------------------------------------




        ## signal handling
        
        self.light.exposure.valueChanged.connect(self.receivedSignal)    



# ------------------------------------------------------------------------------------------


    ## methods
        
    def receivedSignal(self, value:float, isActive:bool):
        print(f"Signal reçu : Valeur = {value}, Actif = {isActive}")
        


        