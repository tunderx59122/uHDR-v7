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
import numpy as np, copy
from typing_extensions import Self
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QLineEdit, QCheckBox, QWidget
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QIntValidator

from guiQt.ImageWidget import ImageWidget
from guiQt.ChannelSelector import ChannelSelector
from core import colourData, colourSpace
# ------------------------------------------------------------------------------------------
class LchSelector(QFrame):
    # class attributes

    # constructor
    def __init__(self : Self) -> None:
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        # attributes
        self.active : bool = True
        self.hueRange : tuple[int, int] = (0, 360+90)
        self.chromaRange : tuple[int, int] = (0, 100)
        self.LightnessRange : tuple[int, int] = (0,200)

        ## layout
        self.topLayout : QVBoxLayout = QVBoxLayout()
        self.setLayout(self.topLayout)

        ### container
        self.colourView : QFrame = QFrame()
        self.colourView.setFrameShape(QFrame.Shape.StyledPanel)
        self.containerLayout : QHBoxLayout = QHBoxLayout()
        self.colourView.setLayout(self.containerLayout)
       
        ##### ch view
        self.chromaHue : ImageWidget = ImageWidget(np.ones((300,300,3))*.5)
        self.chromaHue.setMinimumSize(200,200)

        ### Lh view
        self.lightnessHue : ImageWidget = ImageWidget(np.ones((300,300,3))*.5)
        self.lightnessHue.setMinimumSize(200,200)

        ##### add to layout
        self.containerLayout.addWidget(self.chromaHue) 
        self.containerLayout.addWidget(self.lightnessHue) 

        ### hue
        hueBarLch : np.ndarray = colourData.buildLchcolourData((75,75), (100,100), (0,360+90), (20,720), width='h', height='c')
        hueBarRGB : np.ndarray = colourSpace.Lch_to_sRGB(hueBarLch,apply_cctf_encoding=True, clip=True)
        self.hueSelector : ChannelSelector = ChannelSelector('hue',hueBarRGB, (0,360+90),(0,360+90))   

        ### chroma
        chromaBarLch : np.ndarray = colourData.buildLchcolourData((75,75), (0,100), (180,180), (20,720), width='c', height='L')
        chromaBarRGB : np.ndarray= colourSpace.Lch_to_sRGB(chromaBarLch,apply_cctf_encoding=True, clip=True)    
        self.chromaSelector : ChannelSelector = ChannelSelector('chroma',chromaBarRGB, (0,100),(0,100)) 

        ### lightness  
        lightnessBarLch : np.ndarray = colourData.buildLchcolourData((0,200), (0,0), (180,180), (20,720), width='L', height='c')
        lightnessBarRGB : np.ndarray = colourSpace.Lch_to_sRGB(lightnessBarLch,apply_cctf_encoding=True, clip=True)
        self.lightnessSelector : ChannelSelector = ChannelSelector('lightness',lightnessBarRGB, (0,200),(0,150)) 

        ### show selction
        self.showSelection : QCheckBox = QCheckBox("show selction")

        ### active checkbox
        self.checkBoxActive : QCheckBox = QCheckBox("active")
        self.checkBoxActive.setChecked(True)

        ### container checkbox
        self.containerCheckbox : QWidget = QWidget()
        self.layoutCheckBox : QHBoxLayout = QHBoxLayout()
        self.containerCheckbox.setLayout(self.layoutCheckBox)
        self.layoutCheckBox.addWidget(self.showSelection)
        self.layoutCheckBox.addStretch()
        self.layoutCheckBox.addWidget(self.checkBoxActive)

        ### add widget to layout
        self.topLayout.addWidget(self.colourView)
        self.topLayout.addWidget(self.hueSelector)
        self.topLayout.addWidget(self.chromaSelector)
        self.topLayout.addWidget(self.lightnessSelector)
        self.topLayout.addWidget(self.containerCheckbox)

        ## calbacks
        self.hueSelector.valuesChanged.connect(self.CBhueSelectionChanged)
        self.chromaSelector.valuesChanged.connect(self.CBchromaSelectionChanged)
        self.lightnessSelector.valuesChanged.connect(self.CBlightnessSelctionChanged)

    # methods
    ## callbacks
    def CBhueSelectionChanged(self: Self) -> None :
        hueMin, hueMax = self.hueSelector.getValues()
        hue : int  = (hueMin + hueMax)//2
        self.hueRange = (hueMin, hueMax)
        # compute chroma bar
        chromaBarLch : np.ndarray = colourData.buildLchcolourData((75,75), (0,100), (hue,hue), (20,720), width='c', height='L')
        chromaBarRGB : np.ndarray= colourSpace.Lch_to_sRGB(chromaBarLch,apply_cctf_encoding=True, clip=True)
        self.chromaSelector.imageWidget.setPixmap(chromaBarRGB)
        self.updateView()

    def CBchromaSelectionChanged(self: Self) -> None :
        self.chromaRange = self.chromaSelector.getValues()
        self.updateView()

    def CBlightnessSelctionChanged(self: Self) -> None:
        self.LightnessRange = self.lightnessSelector.getValues()
        self.updateView()

    # update view
    def updateView(self: Self) -> None:
        # chrmaHue
        chromaHueLCh : np.ndarray = colourData.buildLchcolourData((75,75), self.chromaRange, self.hueRange, (200,200), width='h', height='c')
        chromaHueRGB : np.ndarray= colourSpace.Lch_to_sRGB(chromaHueLCh,apply_cctf_encoding=True, clip=True)
        self.chromaHue.setPixmap(chromaHueRGB)
        # chromaLightness
        chromaLightnessLch : np.ndarray = colourData.buildLchcolourData(self.LightnessRange, self.chromaRange, self.hueRange, (200,200), width='h', height='L')
        chromaLightnessRGB : np.ndarray= colourSpace.Lch_to_sRGB(chromaLightnessLch,apply_cctf_encoding=True, clip=True)
        self.lightnessHue.setPixmap(chromaLightnessRGB)
