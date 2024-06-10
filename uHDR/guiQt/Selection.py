from __future__ import annotations
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
from PyQt6.QtWidgets import QFrame,QVBoxLayout 
from PyQt6.QtCore import pyqtSignal
import copy
from guiQt.ScoringSelection import ScoringSelection

# -------------------------------------------------------------------------------------------
# --- ScoringSelection (QFrame) -------------------------------------------------------------
# -------------------------------------------------------------------------------------------
debug = False
class Selection(QFrame):
    """gui of selection panel."""
    # class attributes
    ## signal
    scoreSelectionChanged : pyqtSignal = pyqtSignal(list)

    # constructor
    # -----------------------------------------------------------------------------

    def __init__(self: Selection) -> None: 
        super().__init__()

        # attributes
        self.topLayout : QVBoxLayout = QVBoxLayout() ; self.setLayout(self.topLayout)
        self.selectByScore : ScoringSelection = ScoringSelection('score:', 6)

        self.topLayout.addWidget(self.selectByScore)
        self.topLayout.addStretch()

        ## callbacks
        self.selectByScore.selectionChanged.connect(self.CBscoreSlectionChanged)

    # methods
    # -----------------------------------------------------------------------------
    ## callbacks
    def CBscoreSlectionChanged(self : Selection, scores : list[bool]) -> None:
        """called when score selection changed."""
        if debug : print(f'guiQt.Selection.CBscoreSelectionChanged({scores})')
        self.scoreSelectionChanged.emit(copy.deepcopy(scores))