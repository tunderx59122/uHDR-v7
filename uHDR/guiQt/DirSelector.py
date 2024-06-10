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
from PyQt6.QtWidgets import QFileDialog


# ------------------------------------------------------------------------------------------
# --- class DirSelector --------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
class DirSelctor:

    def callBackSelectDir(self):
        """Callback of export HDR menu: open file dialog, store image filenames (self.imagesName), set directory to model
        """
        pass
        # if pref.verbose: print(" [CONTROL] >> AppController.callBackSelectDir()")
        # dirName = QFileDialog.getExistingDirectory(None, 'Select Directory', self.model.directory)
        # if dirName != "":
        #     # save current images (metadata)
        #     self.view.imageGalleryController.save()
        #     # get images in the selected directory
        #     self.imagesName = []; self.imagesName = list(self.model.setDirectory(dirName))

        #     self.view.imageGalleryController.setImages(self.imagesName)
        #     self.hdrDisplay.displaySplash()