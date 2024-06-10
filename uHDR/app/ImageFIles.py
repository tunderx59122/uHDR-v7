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
import os
from matplotlib import image as imagePLT
from core.image import Image, filenamesplit
from numpy import ndarray
from PyQt6.QtCore import QObject, pyqtSignal, QThreadPool, QRunnable
from app.Jexif import Jexif
from app.Tags import Tags
from app.Score import Score
from core.image import Image
from preferences.Prefs import Prefs
# ------------------------------------------------------------------------------------------
# --- class ImageFiles(QObject) -----------------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = False
class ImageFiles(QObject):
    """ manages image files in the directory: asynchronous loading, caching images."""
    # class attributes
    # -----------------------------------------------------------------
    imageLoaded : pyqtSignal = pyqtSignal(str)

    # constructor
    # -----------------------------------------------------------------
    def __init__(self: ImageFiles) -> None: 
        super().__init__()
    
        # could be overwrite by setPrefs methods
        self.imagePath : str = '.'          # default image path
        self.extraPath : str = '.uHDR'      # default extra path

        self.nbImages : int = 0

        self.imageFilenames : list[str] = []
        self.imageIsLoaded : dict[str, bool] = {}
        self.imageIsThumbnail : dict[str, bool] = {}
        
        self.images : dict[str, ndarray] = {}

        ## score
        self.imageScore : dict[str,int] = {}

        ## tags
        self.imageTags : dict[str, Tags] = {}
        ## exif in json
        self.imageExif : dict[str,dict[str,str]] = {}
        
        # thread pool
        self.pool = QThreadPool.globalInstance() # get a global pool

    # methods
    # -----------------------------------------------------------------
    def reset(self: ImageFiles):
        self.imageFilenames     = []
        self.imageIsLoaded      = {}

        self.imageIsThumbnail   = {}

        self.images             = {}

        self.imageScore         = {}
        self.imageTags          = {}
        self.imageExif          = {}

    # -----------------------------------------------------------------
    def __repr__(self: ImageFiles) -> str:
        res ='-------------------  imageFiles -------------------------------'
        res+=f'\n image path: {self.imagePath}'
        res+=f'\n extra path: {self.extraPath}'
        res+=f'\n nb images: {self.nbImages}'
        res+=f'\n filenames: {self.imageFilenames}'
        res+=f'\n images: '
        for file in self.imageFilenames:
            res += f'\n\t "{file}" > loaded: {self.imageIsLoaded[file]}'
            res += f'\n\t "{file}" > exif: {self.imageExif[file] if file in self.imageExif.keys() else "not loaded"}' 
            res += f'\n\t "{file}" > score: {self.imageScore[file] if file in self.imageExif.keys() else "not loaded"}' 
            res += f'\n\t "{file}" > tags: {self.imageTags[file] if file in self.imageTags.keys() else "not loaded"}' 
        res +='\n-------------------  imageFiles End ----------------------------'

        return res

    # -----------------------------------------------------------------
    def getNbImages(self: ImageFiles) -> int : 
        """return the number of image files."""
        return len(self.imageFilenames)

    # -----------------------------------------------------------------
    def getImagesFilesnames(self: ImageFiles) -> list[str]: 
        """return the list of image files."""
        return self.imageFilenames
    
    # -----------------------------------------------------------------
    def setPrefs(self:ImageFiles) -> None:
        """update attributes according preferences."""
        self.imagePath = Prefs.currentDir
        self.extraPath = Prefs.extraPath
    
    # -----------------------------------------------------------------    
    def setDirectory(self: ImageFiles, dirPath: str) -> int:
        """set directory: scan for image files"""

        if debug : print(f'ImageFiles.setDirectory({dirPath})')

        self.reset()
        self.imagePath = dirPath
        # scan directory
        ext : tuple[str]= tuple(Prefs.imgExt)
        filenames = sorted(os.listdir(dirPath))
        self.imageFilenames = list(filter(lambda x: x.endswith(ext),filenames))
        self.nbImages = len(self.imageFilenames)

        for filename in self.imageFilenames: self.imageIsLoaded[filename] = False

        # preload exif, score, tags, ...
        self.checkExtra()

        for filename in self.imageFilenames:
            # tags
            self.imageTags[filename] = Tags.load(self.imagePath, filename, self.extraPath)
            # jexif
            self.imageExif[filename] = Jexif.load(self.imagePath, filename, self.extraPath)
            # score
            self.imageScore[filename] = Score.load(self.imagePath, filename, self.extraPath)

            

        return len(self.imageFilenames)
    
    # -----------------------------------------------------------------
    def requestLoad(self: ImageFiles, filename: str, thumbnail : bool=True): 
        """add a image loading request to pool thread."""

        if debug : print(f'ImageFiles.requestLoad({filename}, thumbnail={thumbnail})')

        if self.imageIsLoaded[filename] != True:
            # extra
            self.imageTags[filename] = Tags.load(self.imagePath, filename, self.extraPath)
            # jexif
            self.imageExif[filename] = Jexif.load(self.imagePath, filename, self.extraPath)
            # score
            self.imageScore[filename] = Score.load(self.imagePath, filename, self.extraPath)


            # image
            filename_ = os.path.join(self.imagePath,filename)
            self.pool.start(RunLoadImage(self,filename_, thumbnail))
        else:
            self.imageLoaded.emit(filename)
    
    # -----------------------------------------------------------------
    def endLoadImage(self : ImageFiles,error: bool, filename: str):
        """"called when an image is loaded."""
    
        if debug : print(f'ImageFiles.endLoadImage( error={error}, {filename})')

        if not error:
            filename = filename.split('\\')[-1]
            self.imageIsLoaded[filename] = True 

            self.imageLoaded.emit(filename)


        else:
            self.requestLoad(filename)  
    
    # -----------------------------------------------------------------
    def getImage(self: ImageFiles, name: str, thumbnail : bool = True) -> ndarray:
        """get image, assumption image is loaded"""

        return self.images[name]
    
    # -----------------------------------------------------------------
    def getImageTags(self: ImageFiles, name : str) -> Tags: 
        return self.imageTags[name]
    
    # -----------------------------------------------------------------
    def getImageExif(self: ImageFiles, name : str) -> dict[str,str]: 
        return self.imageExif[name]
    
    # -----------------------------------------------------------------
    def getImageScore(self: ImageFiles, name : str) ->int: 
        return self.imageScore[name]
    
    # -----------------------------------------------------------------   
    def checkExtra(self: ImageFiles) -> None:
        ePath: str = os.path.join(self.imagePath, self.extraPath) 
        if os.path.exists(ePath):
            pass
        else:
            os.mkdir(ePath)
    
    # -----------------------------------------------------------------
    def updateImageTag(self, imageName: str, type: str, name: str, value: bool) -> None:


        self.imageTags[imageName].add(type, name, value)
        self.imageTags[imageName].save(self.imagePath, self.extraPath, imageName)
    
    # -----------------------------------------------------------------
    def updateImageScore(self: ImageFiles, imageName: str, value: int) -> None:


        self.imageScore[imageName] = value

        Score.save(self.imagePath, self.extraPath, imageName,self.imageScore[imageName])

# ------------------------------------------------------------------------------------------
# --- RunLoadImage(QRunnable) --------------------------------------------------------------
# ------------------------------------------------------------------------------------------
class RunLoadImage(QRunnable):
    def __init__(self: RunLoadImage,parent: ImageFiles, filename:str, thumbnail :bool = True):

        super().__init__()
        self.parent: ImageFiles = parent
        self.filename : str = filename
        self.thumbnail : bool = thumbnail
    
    # -----------------------------------------------------------------
    def run(self:RunLoadImage):

        if debug : print(f'RunLoadImage.run({self.filename})')

        try:
            # first check file exists ?
            if os.path.exists(self.filename):

                # thumbnail ?
                if self.thumbnail : # thumbnail not original image

                    # thumbnail exitsts ?
                    path, name, ext = filenamesplit(self.filename)
                    thumbnailName : str = os.path.join(path, Prefs.extraPath, Prefs.thumbnailPrefix+name+'.'+ext)
                    
                    if os.path.exists(thumbnailName):
                        imageSmall : Image = Image.read(thumbnailName)
                    else:
                        imageBig : Image = Image.read(self.filename)
                        imageSmall : Image = imageBig.buildThumbnail(Prefs.thumbnailMaxSize)
                        imageSmall.write(thumbnailName)
                    
                    #set thumbnail to parent <class ImageFiles>
                    self.parent.images[self.filename.split('\\')[-1]] = imageSmall.cData 

                else: # original image not thumbnail

                    imageBig = Image.read(self.filename)
                    self.parent.images[self.filename.split('\\')[-1]] = imageBig.cData              
            
            self.parent.endLoadImage(False, self.filename)
        except(IOError, ValueError) as e:
            self.parent.endLoadImage(True, self.filename)
    # -----------------------------------------------------------------
# ------------------------------------------------------------------------------------------

 