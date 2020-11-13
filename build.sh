#!/bin/bash

./FF_HOI.py Example.sfd
fontmake --verbose INFO -m FRBFontForgeHOIExample.designspace -o variable --keep-overlaps --optimize-cff 0 --no-optimize-gvar --keep-direction --output-path HOI.ttf
./mangle_ttf.py

mv HOI.ttf dist/HOI_unmangled.ttf
mv HOI2.ttf dist/HOI.ttf
