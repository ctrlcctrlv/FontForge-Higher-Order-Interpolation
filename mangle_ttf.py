#!/usr/bin/env python3
from lib.util import *
import fontTools.ttLib
ttf=fontTools.ttLib.TTFont(file='NLI.ttf')
for a in ttf["fvar"].axes: a.axisTag = '0001'
for a in ttf["STAT"].table.DesignAxisRecord.Axis: a.AxisTag = '0001'

for nr in ttf["name"].names:
    names = {1033: b'\x001', 0: b'1'}

    if nr.nameID in [256, 257, 258]:
        nr.string = names[nr.langID]

ttf.save('NLI2.ttf')
eprint("Successfully mangled!")
