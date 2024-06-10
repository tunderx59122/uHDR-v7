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

from numpy import ndarray
from app.Jexif import Jexif

import preferences.Prefs
from guiQt.MainWindow import MainWindow
from app.ImageFIles import ImageFiles
from app.Tags import Tags
from app.SelectionMap import SelectionMap

# ------------------------------------------------------------------------------------------
# --- class App ----------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = True
class App:
    # static attributes

    # constructor
    def __init__(self: App) -> None:
        """uHDR v7 application"""
        # loading preferences
        preferences.Prefs.Prefs.load()

        ## -----------------------------------------------------
        ## ------------         attributes          ------------
        ## -----------------------------------------------------        
        
        ## image file management
        self.imagesManagement : ImageFiles = ImageFiles()
        self.imagesManagement.imageLoaded.connect(self.CBimageLoaded)
        self.imagesManagement.setPrefs()
        self.imagesManagement.checkExtra()
        nbImages : int = self.imagesManagement.setDirectory(preferences.Prefs.Prefs.currentDir)

        # read image tags in directory
        allTagsInDir : dict[str, dict[str,bool]] =  Tags.aggregateTagsFiles(preferences.Prefs.Prefs.currentDir,preferences.Prefs.Prefs.extraPath)
        
        # merge with default tags from preferences
        self.tags : Tags = Tags(Tags.aggregateTagsData([preferences.Prefs.Prefs.tags, allTagsInDir]))
        
        ## selection
        self.selectionMap :  SelectionMap = SelectionMap(self.imagesManagement.getImagesFilesnames())

        ## current selected image
        self.selectedImageIdx : int | None = None

        ## -----------------------------------------------------
        ## ------------             gui             ------------
        ## -----------------------------------------------------

        self.mainWindow : MainWindow = MainWindow(nbImages, self.tags.toGUI())
        self.mainWindow.showMaximized()
        self.mainWindow.show()

        ## callbacks
        self.mainWindow.dirSelected.connect(self.CBdirSelected)
        self.mainWindow.requestImages.connect(self.CBrequestImages)
        self.mainWindow.imageSelected.connect(self.CBimageSelected)

        self.mainWindow.tagChanged.connect(self.CBtagChanged)
        self.mainWindow.scoreChanged.connect(self.CBscoreChanged)

        self.mainWindow.scoreSelectionChanged.connect(self.CBscoreSelectionChanged)

        self.mainWindow.setPrefs()

    # methods
    # -----------------------------------------------------------------

    ##  getImageRangeIndex
    ## ----------------------------------------------------------------
    def getImageRangeIndex(self: App) -> tuple[int,int]: 
        """return the index range (min index, max index) of images displayed by the gallery."""

        return self.mainWindow.imageGallery.getImageRangeIndex()

    ##  update
    ## ----------------------------------------------------------------
    def update(self: App) -> None:
        """call to update gallery after selection changed or directory changed."""
        # number of image in current pages 
        minIdx, maxIdx = self.getImageRangeIndex()
        self.mainWindow.setNumberImages(self.selectionMap.getSelectedImageNumber()) 
        self.mainWindow.setNumberImages(maxIdx - minIdx) 
        self.CBrequestImages(minIdx, maxIdx)

    ## -----------------------------------------------------------------------------------------------------
    ## app logic: callbacks 
    ## -----------------------------------------------------------------------------------------------------

    #### select new directory
    #### -----------------------------------------------------------------
    def CBdirSelected(self: App, path:str) -> None:
        """callback: called when directory is selected."""

        # ------------- DEBUG -------------
        if debug : 
            print(f'App.CBdirSelected({path})')
        # ------------- ------ -------------  

        self.imagesManagement.setDirectory(path)
        self.selectionMap.setImageNames(self.imagesManagement.getImagesFilesnames())
        self.selectionMap.selectAll()

        # reset gallery 
        self.mainWindow.resetGallery()
        self.mainWindow.setNumberImages(self.imagesManagement.getNbImages())
        self.mainWindow.firstPage()

    #### request image: zoom or page changed
    #### -----------------------------------------------------------------
    def CBrequestImages(self: App, minIdx: int , maxIdx:int ) -> None:
        """callback: called when images are requested (occurs when page or zoom level is changed)."""

        imagesFilenames : list[str] = self.imagesManagement.getImagesFilesnames()

        for sIdx in range(minIdx, maxIdx+1):

            gIdx : int|None = self.selectionMap.selectedlIndexToGlobalIndex(sIdx) 

            if gIdx != None: self.imagesManagement.requestLoad(imagesFilenames[gIdx])
            else: self.mainWindow.setGalleryImage(sIdx, None)


    #### image loaded
    #### -----------------------------------------------------------------
    def CBimageLoaded(self: App, filename: str):
        """"callback: called when requested image is loaded (asynchronous loading)."""


        image : ndarray = self.imagesManagement.images[filename]
        imageIdx = self.selectionMap.imageNameToSelectedIndex(filename)         

        if imageIdx != None: self.mainWindow.setGalleryImage(imageIdx, image)


    #### image selected
    #### -----------------------------------------------------------------
    def CBimageSelected(self: App, index):


        self.selectedImageIdx = index # index in selection

        gIdx : int | None= self.selectionMap.selectedlIndexToGlobalIndex(index)# global index

        if (gIdx != None):

            image : ndarray = self.imagesManagement.getImage(self.imagesManagement.getImagesFilesnames()[gIdx])
            tags : Tags = self.imagesManagement.getImageTags(self.imagesManagement.getImagesFilesnames()[gIdx])
            exif : dict[str,str] = self.imagesManagement.getImageExif(self.imagesManagement.getImagesFilesnames()[gIdx])
            score : int = self.imagesManagement.getImageScore(self.imagesManagement.getImagesFilesnames()[gIdx])

            self.mainWindow.setEditorImage(image)

            # update image info
            imageFilename : str =  self.imagesManagement.getImagesFilesnames()[gIdx] 
            imagePath : str =  self.imagesManagement.imagePath 
            #### if debug : print(f'App.CBimageSelected({index}) > path:{imagePath}')

            self.mainWindow.setInfo(imageFilename, imagePath, *Jexif.toTuple(exif))

            self.mainWindow.setScore(score)

            # update tags info
            self.mainWindow.resetTags()
            if tags:
                self.mainWindow.setTagsImage(tags.toGUI())

    #### tag changed
    #### -----------------------------------------------------------------
    def CBtagChanged(self, key: tuple[str, str], value : bool) -> None:


        if self.selectedImageIdx != None:
            imageName : str|None = self.selectionMap.selectedIndexToImageName(self.selectedImageIdx)
            if debug : print(f'\t\t imageName:{imageName}')
            if imageName != None : self.imagesManagement.updateImageTag(imageName, key[0], key[1], value)
    
    #### score changed
    #### -----------------------------------------------------------------
    def CBscoreChanged(self, value : int) -> None:


        if self.selectedImageIdx != None:
            imageName : str|None = self.selectionMap.selectedIndexToImageName(self.selectedImageIdx)

            if imageName != None : self.imagesManagement.updateImageScore(imageName, value)


    ### score selection changed
    ### ------------------------------------------------------------------
    def CBscoreSelectionChanged(self: App, listSelectedScore : list[bool]) -> None:
        """called when selection changed."""


        # get {'image name': score}
        imageScores : dict[str, int] = self.imagesManagement.imageScore
        # selected score
        selectedScores : list[int] = []
        for i, selected in enumerate(listSelectedScore) :  
            if selected : selectedScores.append(i)
        # send info to selectionMap
        self.selectionMap.selectByScore(imageScores, selectedScores)
        self.update()
# ------------------------------------------------------------------------------------------
