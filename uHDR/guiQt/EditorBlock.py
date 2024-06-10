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

from numpy import ndarray

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSplitter
from PyQt6.QtGui import QDoubleValidator, QIntValidator 
from PyQt6.QtCore import Qt, pyqtSignal, QLocale

from guiQt.Editor import Editor
from guiQt.ImageWidget import ImageWidget

# ------------------------------------------------------------------------------------------
# --- class EditorBlock (QSplitter) ------------------------------------------------------
# ------------------------------------------------------------------------------------------
class EditorBlock(QSplitter):
    # class attributes
    ## signal

    # constructor
    def __init__(self:Self) -> None:
        super().__init__(Qt.Orientation.Vertical)

        # attributes
        self.imageWidget : ImageWidget = ImageWidget() 
        self.edit : Editor = Editor()

        # adding widgets to self (QSplitter)
        self.addWidget(self.imageWidget)
        self.addWidget(self.edit)
        self.setSizes([20,80])

    # methods
    ## setImage
    def setImage(self: Self, image: ndarray | None):
        self.imageWidget.setPixmap(image)

        