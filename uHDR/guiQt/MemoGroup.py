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
import sys
from typing_extensions import Self
from PyQt6.QtWidgets import QFrame, QPushButton, QTextEdit, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, pyqtSignal, QLocale
from guiQt.MemoLine import MemoLine
# ------------------------------------------------------------------------------------------
# --- class MemoGroup(QFrame) ---------------------------------------------------------------
# ------------------------------------------------------------------------------------------
class MemoGroup (QFrame):
    # class attributes
    ## signal

    # constructor
    def __init__(self: Self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)

        # attributes
        ## layout and widgets
        self.topLayout : QVBoxLayout = QVBoxLayout()
        self.setLayout(self.topLayout)

        self.mem0 : MemoLine = MemoLine('slot[0]')
        self.mem1 : MemoLine = MemoLine('slot[1]')
        self.memTextEdit : QTextEdit = QTextEdit('message')

        self.topLayout.addWidget(self.mem0)
        self.topLayout.addWidget(self.mem1)
        self.topLayout.addWidget(self.memTextEdit)
# ------------------------------------------------------------------------------------------


