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
from PyQt6.QtWidgets import QVBoxLayout, QFrame
from PyQt6.QtCore import pyqtSignal

from guiQt.AdvanceLineEditGroup import AdvanceLineEditGroup

# -------------------------------------------------------------------------------------------
# --- InfoBase (QFrame) ---------------------------------------------------------------------
# -------------------------------------------------------------------------------------------
debug : bool = False
class InfoBase(QFrame):
    # class attributes
    ## signal

    # constructor
    def __init__(self: Self) -> None:
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)     

        # attributes
        self.name : str = " ... "
        self.path : str = " ... " 
        self.size : tuple[int,int] = (-1,-1)
        self.colorSpace : str = ''
        self.type : str =  ''
        self.bitPerSample : int = -1

        ## widget: AdvanceLineEditGroup
        self.topLayout : QVBoxLayout = QVBoxLayout()
        self.setLayout(self.topLayout)
        self.baseInfo :  AdvanceLineEditGroup = AdvanceLineEditGroup( self.toGui())
        self.topLayout.addWidget(self.baseInfo)

    # methods
    def toGui(self: Self) -> dict:
        res : dict = {}

        res["Name: "] = (self.name, False) 
        res["Path: "] = (self.path, False) 
        res["Size (pixel): "] = ((str(self.size[0])) if self.size[0] != -1 else '...' + 
                                ' x '+ 
                                (str(self.size[1]) if self.size[1] != -1 else '...'), False)
        res["Color Space: "] = (self.colorSpace if self.colorSpace != '' else '...', False)
        res["Type: "] = (self.type if self.type != '' else '...', False)
        res["Bit per sample: "] = (str(self.bitPerSample) if self.bitPerSample != -1 else "...", False)

        return res

    def setInfo(self: Self, name: str, path: str, size : tuple[int,int] =(-1,-1), colorSpace : str = '...', type: str ='...', bps : int =-1) -> None:
        if debug : print(f'InfoBase.setInfo({name}, {path} ,{size}, {colorSpace},{type},{bps})')
        self.name = name
        self.path = path
        self.size = size
        self.colorSpace = colorSpace
        self.type = type
        self.bitPerSample = bps
        self.baseInfo.setText([self.name, self.path, 
            (str(self.size[0]) if self.size[0] != -1 else '...' )+ ' x '+( str(self.size[1]) if self.size[1] != -1 else '...'),
            self.colorSpace, self.type, str(self.bitPerSample) if self.bitPerSample != -1 else '...'])


# -------------------------------------------------------------------------------------------


