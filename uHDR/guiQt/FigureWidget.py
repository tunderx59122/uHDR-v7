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
from typing import Any
from typing_extensions import Self

from PyQt6.QtWidgets import QWidget, QLabel, QMainWindow, QSplitter, QFrame, QDockWidget
from PyQt6.QtWidgets import QSplitter, QFrame, QSlider, QCheckBox, QGroupBox
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QGridLayout, QLayout, QScrollArea, QFormLayout
from PyQt6.QtWidgets import QPushButton,QLineEdit, QComboBox, QSpinBox
from PyQt6.QtGui import QPixmap, QImage, QResizeEvent
from PyQt6.QtCore import Qt
import numpy as np

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from  matplotlib.axes import Axes

import time
import math
import functools

# ------------------------------------------------------------------------------------------
# --- class FigureWidget(FigureCanvas) -----------------------------------------------------
# ------------------------------------------------------------------------------------------

class FigureWidget(FigureCanvas):
    """ Matplotlib Figure Widget  """

    def __init__(self : Self, width : int = 5, height : int = 5):
        # create Figure
        self.fig  : Figure = Figure()
        self.axes : Axes = self.fig.add_subplot(111) 
        FigureCanvas.__init__(self, self.fig)    # explicite call of super constructor
        FigureCanvas.updateGeometry(self)
        self.setMinimumSize(200, 200)

    def plot(self : Self ,X :np.ndarray , Y : np.ndarray, mode : str, clear :bool =False):

        if clear: self.axes.clear()
        self.axes.plot(X,Y,mode)
        
        try:
            self.fig.canvas.draw()
        except Exception:
            time.sleep(0.5)
            self.fig.canvas.draw()


# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    app : QApplication = QApplication(sys.argv)
    iW : FigureWidget = FigureWidget()
    iW.setMinimumHeight(500)
    iW.show()
    iW.plot(np.array([0,1,1,0,0]),np.array([0,0,1,1,0]),'r--')
    iW.plot(np.array([0.5]),np.array([0.5]),'b*')

    sys.exit(app.exec())

