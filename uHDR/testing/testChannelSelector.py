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
from core import colourData, colourSpace
from guiQt.ChannelSelector import ChannelSelector
# ------------------------------------------------------------------------------------------
# test
# ------------------------------------------------------------------------------------------
def test() -> ChannelSelector:
    hueBarLch = colourData.buildLchcolourData((75,75), (100,100), (0,360), (20,720), width='h', height='c')
    hueBarRGB = colourSpace.Lch_to_sRGB(hueBarLch,apply_cctf_encoding=True, clip=True)

    def cb(name: str, min:int, max:int) -> None : print(f'/§\\ {name}::[{min},{max}]')

    testCS : ChannelSelector = ChannelSelector('hue',hueBarRGB, (0,360),(10,350))
    testCS.valuesChanged.connect(cb)
    return testCS
# ------------------------------------------------------------------------------------------