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
import os, json
# ------------------------------------------------------------------------------------------
# --- class Score --------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
debug : bool = False
# ------------------------------------------------------------------------------------------
class Score:
    """image score: {'score': int in[0,5]}.

    
        future: could include 'date': and/or 'author'
     """

    # methods
    # -----------------------------------------------------------------------------
    @staticmethod
    def load(imageDir: str, imageFilename: str, extraDir : str) -> int:
        # check if extra '.uHDR' dir exist
        extraPath = os.path.join(imageDir, extraDir) 
        if os.path.isdir(extraPath):
            scoreFilename= os.path.join(imageDir,extraDir,imageFilename[:-3]+'score') 
            if os.path.exists(scoreFilename):
                with open(scoreFilename) as scoreFile:
                    scoreDict : dict[str, int] =  json.load(scoreFile)
                    if 'score' in scoreDict.keys() : 
                        score : int = scoreDict['score']
                        return score
                    else:
                        print(f'[ERROR] score not find in "{scoreFilename}", score set to: 0"')
                        return 0
            else: # scoreFile not found
                scoreDict : dict[str, int] = {'score': 0}
                with open(scoreFilename,'w') as scoreFile:  json.dump(scoreDict, scoreFile)
                print(f'[ERROR] file "{scoreFilename}" not found, score set to: 0"')
                return 0
        return 0

    ## save score to file
    ## -------------------------------------------------------
    @staticmethod
    def save(imageDir: str, extraDir: str, imageFilename : str, score:int) -> None:
        if debug : print(f'app.Score.save({imageDir},{extraDir},{imageFilename})')
        # check if extra '.uHDR' dir exist
        extraPath = os.path.join(imageDir, extraDir) 
        if os.path.isdir(extraPath):
            scoreFilename= os.path.join(imageDir,extraDir,imageFilename[:-3]+'score') 
            with open(scoreFilename,'w') as file:
                if debug : print(f'app.Score.save({imageDir},{extraDir},{imageFilename}) > {score}')
                json.dump({'score': score}, file)   
