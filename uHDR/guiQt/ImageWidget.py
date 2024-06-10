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
# -----------------------------------------------------------------------------
from typing_extensions import Self
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap, QImage, QResizeEvent
from PyQt6.QtCore import Qt
import numpy as np

# ------------------------------------------------------------------------------------------
# --- class ImageWidget(QWidget) -------------------------------------------------------
# ------------------------------------------------------------------------------------------
class ImageWidget(QWidget):

    def __init__(self: Self,colorData : np.ndarray|None = None) -> None:
        super().__init__()

        self.label : QLabel = QLabel(self)   # create a QtLabel for pixmap
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        if not isinstance(colorData, np.ndarray): colorData = ImageWidget.emptyImageColorData()
        self.imagePixmap : QPixmap
        self.setPixmap(colorData)  

    # methods
    # -------------------------------------------------- 
    def resize(self : Self)-> None:
        self.label.resize(self.size())
        self.label.setPixmap(self.imagePixmap.scaled(self.size(),Qt.AspectRatioMode.KeepAspectRatio))

    # -------------------------------------------------- 
    def resizeEvent(self : Self,event :QResizeEvent)-> None:
        self.resize()
        super().resizeEvent(event)

    # -------------------------------------------------- 
    def setPixmap(self: Self, colorData :  np.ndarray|None = None) -> QPixmap:
        if not isinstance(colorData, np.ndarray): colorData = ImageWidget.emptyImageColorData()

        height, width , channel  = colorData.shape   
        bytesPerLine = channel * width

        # clip
        colorData[colorData>1.0] = 1.0
        colorData[colorData<0.0] = 0.0

        qImg : QImage= QImage(bytes((colorData*255).astype(np.uint8)), width, height, bytesPerLine, QImage.Format.Format_RGB888) # QImage
        self.imagePixmap : QPixmap = QPixmap.fromImage(qImg)
        self.resize()

        return self.imagePixmap

    # -------------------------------------------------- 
    def setQPixmap(self: Self, qPixmap : QPixmap)-> None:
        self.imagePixmap = qPixmap
        self.resize()

    # -------------------------------------------------- 
    @staticmethod
    def emptyImageColorData()-> np.ndarray: return np.ones((90,160,3))*(220/255) 

# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
    from matplotlib.pyplot import imread
    import sys
    from PyQt6.QtWidgets import QApplication
    img : np.ndarray = imread('C:/Users/rcozo/Dropbox/dev/copoc/images/maximus/4.jpg')/255
    app : QApplication = QApplication(sys.argv)
    iW : ImageWidget = ImageWidget()
    iW.setMinimumHeight(55)
    iW.show()

    sys.exit(app.exec())