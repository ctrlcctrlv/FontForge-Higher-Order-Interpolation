#!/bin/bash

./FF_HOI.py Example.sfd
fontmake --verbose INFO -m FRBFontForgeHOIExample.designspace -o variable --keep-overlaps --optimize-cff 0 --no-optimize-gvar --keep-direction --output-path NLI.ttf
./mangle_ttf.py

mv NLI.ttf NLI_unmangled.ttf
mv NLI2.ttf NLI.ttf
