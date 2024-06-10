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
from PyQt6.QtWidgets import QWidget, QScrollArea, QVBoxLayout, QPushButton, QMainWindow
from PyQt6.QtGui import QDoubleValidator, QIntValidator 
from PyQt6.QtCore import Qt, pyqtSignal, QLocale, QSize

from guiQt.ColorEditorBlock import ColorEditorBlock

# ------------------------------------------------------------------------------------------
# --- class ColorBlockScroll (QWidget) -----------------------------------------------------
# ------------------------------------------------------------------------------------------
class ColorBlockScroll(QScrollArea):
    # class attributes
    ## signal

    # constructor
    def __init__(self : Self) -> None:
        super().__init__()


        ## lightblock widget
        self.light : ColorEditorBlock = ColorEditorBlock()
        self.light.setMinimumSize(500,1200)

        ## Scroll Area Properties
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setWidgetResizable(True) 

        self.setWidget(self.light)

# ------------------------------------------------------------------------------------------


