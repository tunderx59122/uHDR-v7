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

from __future__ import annotations
from math import ceil
from typing_extensions import Self
from PyQt6.QtWidgets import QHBoxLayout, QWidget, QSplitter, QPushButton, QLabel, QSlider
from PyQt6.QtCore import pyqtSignal, Qt

from guiQt.ImageGallery import ImageGallery

from numpy import ndarray

# ------------------------------------------------------------------------------------------
# --- class AdvanceImageGallery(QSplitter) -------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = False
class AdvanceImageGallery(QSplitter):
    """ 
    """
    # class attributes
    ## signal
    requestImages : pyqtSignal = pyqtSignal(int,int)
    imageSelected : pyqtSignal = pyqtSignal(int)

    # constructor
    def __init__(self:AdvanceImageGallery, nbImages: int = 0) -> None:

        super().__init__(Qt.Orientation.Vertical)

        # attributes
        self.active : bool = True
        ## gallery size
        self.previousSize : tuple[int,int] = (2,2)
        self.size : tuple[int,int] = (2,2)
        self.deltaSize : float = 1.5
        self.maxColSize : int = 9

        ## pages
        self.pageIndex : int = 0

        ## images
        self.selectedImage : int|None = None
        self.nbImages : int = nbImages

        # gallery part
        self.gallery : ImageGallery = ImageGallery(self.size)

        # control part
        self.navContainer : QWidget = QWidget()
        self.navLayout : QHBoxLayout = QHBoxLayout(); self.navContainer.setLayout(self.navLayout)
        self.previousPage : QPushButton = QPushButton("< previous") ; self.navLayout.addWidget(self.previousPage)
        self.navLayout.addStretch()
        self.one : QPushButton = QPushButton('[    ]') ; self.navLayout.addWidget(self.one)
        self.zoomLabel : QLabel = QLabel("zoom:") ; self.navLayout.addWidget(self.zoomLabel)
        self.zoomMinus : QPushButton = QPushButton("(+)") ; self.navLayout.addWidget(self.zoomMinus)
        self.zoomSlider : QSlider = QSlider(Qt.Orientation.Horizontal)
        self.zoomSlider.setMinimum(1)
        self.zoomSlider.setMaximum(self.maxColSize)
        self.navLayout.addWidget(self.zoomSlider)
        self.zoomPlus : QPushButton = QPushButton("(-)") ; self.navLayout.addWidget(self.zoomPlus)
        self.navLayout.addStretch()
        self.pageLabel : QLabel = QLabel("page: X/XX"); self.navLayout.addWidget(self.pageLabel)
        self.navLayout.addStretch()
        self.nextPage : QPushButton = QPushButton("next >") ; self.navLayout.addWidget(self.nextPage)

        # all parts
        self.addWidget(self.gallery)
        self.addWidget(self.navContainer)
        self.setSizes([1060,20])

        ## signal
        self.zoomMinus.clicked.connect(self.decSize)
        self.zoomPlus.clicked.connect(self.incSize)
        self.zoomSlider.valueChanged.connect(self.zoomSliderChanged)
        self.one.clicked.connect(self.CBOne)

        self.nextPage.clicked.connect(self.CBnextPage)
        self.previousPage.clicked.connect(self.CBpreviousPage)

        self.gallery.imageSelected.connect(self.CBimageSelected)

    # --------------------------------------------------------------------------
    # methods
    # --------------------------------------------------------------------------
    ## gallery size management
    def incSize(self: AdvanceImageGallery) -> None:
        """ zoom out """

        nbRow : int = self.size[0]        
        nbCol : int = self.size[1]

        if nbCol < self.maxColSize : 
            nbCol+=1
            if nbCol > nbRow * self.deltaSize : nbRow += 1
        
        self.size = (nbRow,nbCol) 

        self.active = False
        self.zoomSlider.setValue(nbCol)
        self.active = True

        self.gallery.size = self.size

        minImgIdx, maxImgIdx = self.getImageRangeIndex()
        if not isinstance(self.selectedImage, int):
            imgIdx : int = (minImgIdx+maxImgIdx)//2
        else:
            imgIdx : int = self.selectedImage
        self.pageIndex = self.imageIdxToPageIndex(imgIdx)

        if debug : 
            print(f'AdvanceImageGallery.incSize():')
            print(f'\t page index:{self.pageIndex}') 
            print(f'\t displayed images between:{self.getImageRangeIndex()}')

        self.requestImages.emit(*self.getImageRangeIndex())
        self.updatePageInfo()

    ## -------------------------------------------------------------------------------------------
    def decSize(self: AdvanceImageGallery) -> None:
        if debug : print(f'AdvanceImageGallery.decSize()')
        nbRow : int = self.size[0]        
        nbCol : int = self.size[1]

        if nbCol >  1 : 
            nbCol-=1
            if nbCol <= (nbRow-1) * self.deltaSize : 
                if nbRow > 1 : nbRow -= 1
        
        self.size = (nbRow,nbCol) 

        self.active = False
        self.zoomSlider.setValue(nbCol)
        self.active = True

        self.gallery.size = self.size

        minImgIdx, maxImgIdx = self.getImageRangeIndex()
        if not isinstance(self.selectedImage, int):
            imgIdx : int = (minImgIdx+maxImgIdx)//2
        else:
            imgIdx : int = self.selectedImage
        self.pageIndex = self.imageIdxToPageIndex(imgIdx)

        if debug : 
            print(f'AdvanceImageGallery.decSize():') 
            print(f'\t page index:{self.pageIndex}') 
            print(f'\t displayed images between:{self.getImageRangeIndex()} ')

        self.requestImages.emit(*self.getImageRangeIndex())
        self.updatePageInfo()

    ## -------------------------------------------------------------------------------------------
    def zoomSliderChanged(self:AdvanceImageGallery):

        if debug : print(f'AdvanceImageGallery.zoomSliderChanged() > active: {self.active}')

        if self.active:
            if self.zoomSlider.value() > self.size[1]:
                while self.zoomSlider.value() > self.size[1] : self.incSize()
            elif self.zoomSlider.value() < self.size[1]:
                while self.zoomSlider.value() < self.size[1] : self.decSize()
            self.updatePageInfo()

    ## -------------------------------------------------------------------------------------------
    ## set gallery size
    def setSize(self: AdvanceImageGallery, size : tuple[int,int]) -> None:
        """"set gallery size number of row, number of column"""

        self.size = size
        self.gallery.size = self.size

        self.active = False
        self.zoomSlider.setValue(size[1])
        self.active = True

        self.updatePageInfo()
        
        if debug : print(f'AdvanceImageGallery.setSize({size}) > emit requestImage({self.getImageRangeIndex()})')
        
        self.requestImages.emit(*self.getImageRangeIndex())

    ## -------------------------------------------------------------------------------------------
    ## pages management
    @property
    def nbImgPerPage(self: AdvanceImageGallery) -> int : return self.size[0]*self.size[1]

    ## -------------------------------------------------------------------------------------------
    def getImageRangeIndex(self: Self) -> tuple[int,int]:

        minIdx : int = self.pageIndex*self.nbImgPerPage
        maxIdx :int  = (self.pageIndex+1)*self.nbImgPerPage -1

        if debug : 
            print(f'AdvanceImageGallery.getImageRangeIndex() -> ({minIdx},{maxIdx})')
            print(f'\t self.nbImgPerPage = {self.nbImgPerPage}')

        return minIdx,maxIdx

    ## -------------------------------------------------------------------------------------------
    def CBOne(self: AdvanceImageGallery) -> None:
        """"callback when one 'image' button is clicled"""
        if debug : print(f'AdvanceImageGallery.CBOne():')

        # check current size
        if self.size == (1,1):
            # return to previous size
            if debug : print(f'AdvanceImageGallery.CBOne(): > return to previous size: {self.previousSize}')

            self.size = self.previousSize
            self.gallery.size = self.size

            self.active = False
            self.zoomSlider.setValue(self.size[1])
            self.active = True

            self.pageIndex =   self.imageIdxToPageIndex(self.selectedImage) #type: ignore
            self.updatePageInfo()   
            self.requestImages.emit(*self.getImageRangeIndex())    
            
        else:
            # go to one image page
            self.previousSize = (self.size[0], self.size[1])
            if self.selectedImage != None:
                if debug : print(f'AdvanceImageGallery.CBOne(): > goto one page, index: {self.selectedImage}')
                self.previousSize = self.size
                self.size = (1,1)
                self.gallery.size = self.size

                self.active = False
                self.zoomSlider.setValue(self.size[1])
                self.active = True

                self.pageIndex =   self.imageIdxToPageIndex(self.selectedImage)
                self.updatePageInfo()
                self.requestImages.emit(self.selectedImage, self.selectedImage)
                                
                if debug : print(f'\tAdvanceImageGallery.CBOne(): > goto one page, index: {self.selectedImage} > requestImages.emit({self.selectedImage}, {self.selectedImage})') #####
                
                self.requestImages.emit(self.selectedImage, self.selectedImage)


            else:   # auto select first image in current page
                if debug : print(f'AdvanceImageGallery.CBOne(): > goto one page, index: {self.imageLocalIdxToGlobalIndex(0)}')
                self.CBimageSelected(0)

                self.size = (1,1)
                self.gallery.size = self.size

                self.active = False
                self.zoomSlider.setValue(self.size[1])
                self.active = True


                self.pageIndex =   self.imageIdxToPageIndex(self.selectedImage) #type: ignore
                self.updatePageInfo()
                self.requestImages.emit(self.selectedImage, self.selectedImage)

    ## -------------------------------------------------------------------------------------------
    def firstPage(self:AdvanceImageGallery) -> None : 
        """ firstPage: force to go to first page."""
        if debug : print(f'AdvanceImageGallery.firstPage():')
        
        if self.nbImages > 0:
            self.pageIndex = 0
            self.updatePageInfo()

        self.gallery.resetImages()
        self.requestImages.emit(*self.getImageRangeIndex())
    ## -------------------------------------------------------------------------------------------
    def CBnextPage(self:AdvanceImageGallery) -> None : 
        if debug : print(f'AdvanceImageGallery.CBnextPage():')

        if self.nbImages > 0:
            self.pageIndex = (self.pageIndex +1)%ceil(self.nbImages/self.nbImgPerPage)
            self.updatePageInfo()

        self.gallery.resetImages()
        self.requestImages.emit(*self.getImageRangeIndex())

    ## -------------------------------------------------------------------------------------------
    def CBpreviousPage(self: AdvanceImageGallery) -> None :
        if debug : print(f'AdvanceImageGallery.CBpreviousPage():')

        if self.nbImages > 0:
            self.pageIndex = (self.pageIndex -1)%ceil(self.nbImages/self.nbImgPerPage)  
            self.updatePageInfo()

        self.gallery.resetImages()
        self.requestImages.emit(*self.getImageRangeIndex())

    ## -------------------------------------------------------------------------------------------
    ## number of images in gallery
    def setNbImages(self: AdvanceImageGallery, nb: int) -> None : 
        self.nbImages = nb
        self.updatePageInfo()

    ## -------------------------------------------------------------------------------------------
    ## image local index to global index
    def imageLocalIdxToGlobalIndex(self: AdvanceImageGallery, idxLocal) -> int:
        """return global index of image given by its local index."""
        return self.pageIndex*self.nbImgPerPage+idxLocal

    ## -------------------------------------------------------------------------------------------
    ## image index to page index
    def imageIdxToIndexInPage(self : AdvanceImageGallery, imageIndex : int) -> int:
        """return the index of image in current page."""

        if debug : print(f'AdvanceImageGallery.imageIdxToIndexInPage({imageIndex}) > {imageIndex}%{self.nbImgPerPage} >> {imageIndex%self.nbImgPerPage}')

        return imageIndex%self.nbImgPerPage


    ## -------------------------------------------------------------------------------------------
    def imageIdxToPageIndex(self : AdvanceImageGallery, imageIndex : int) -> int:
        """return the page index of image index."""

        if debug : print(f'AdvanceImageGallery.imageIdxToPageIndex({imageIndex}) > {imageIndex}//{self.nbImgPerPage} >> {imageIndex//self.nbImgPerPage}')

        return imageIndex//self.nbImgPerPage

    ## -------------------------------------------------------------------------------------------
    ## updatepage info
    def updatePageInfo(self :AdvanceImageGallery) -> None:
        maxPage : int = ceil(self.nbImages/self.nbImgPerPage)
        self.pageLabel.setText("page: "+str(self.pageIndex+1)+"/"+str(maxPage))

    ## -------------------------------------------------------------------------------------------
    ## request
    def sendRequestImages(self: AdvanceImageGallery) -> None:
        if debug : print(f'AdvanceImageGallery.sendRequestImages()')
        self.requestImages.emit(*self.getImageRangeIndex())

    ## -------------------------------------------------------------------------------------------
    ## setImage
    def setImage(self:AdvanceImageGallery, index: int, image: ndarray|None) -> None:
        """set an image 'ndarray' in the gallery at 'index' (global index)."""

        if debug : print(f'AdvanceImageGallery.setImage({index}) > {self.imageIdxToIndexInPage(index)} ')

        self.gallery.setImage(self.imageIdxToIndexInPage(index), image)

        # autoselect if one image per page
        if self.nbImgPerPage == 1:
            self.CBimageSelected(0)

    ## -------------------------------------------------------------------------------------------
    ## CBimageSelected
    def CBimageSelected(self: AdvanceImageGallery, idxIW: int) -> None:
        """callback: called when an image is selected."""
        imgIdx : int = self.imageLocalIdxToGlobalIndex(idxIW)

        if imgIdx < self.nbImages:
            self.selectedImage = imgIdx
            
            if debug :  print(f'AdvanceImageGallery.CBimageSelected({idxIW}) -> image index:{self.selectedImage} ')
            
            self.imageSelected.emit(self.selectedImage)

# -------------------------------------------------------------------------------------------

 

