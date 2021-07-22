#!/bin/bash
# Requires: HarfBuzz Dev Tools (hb-view), ImageMagick

for i in `seq -f "%04g" 0 10 1000`; do hb-view --variations="0001=$i,0002=$i,0003=$i" HOI_unmangled.ttf -o $i.png --text-file=../gif-text.txt; echo $i; done
convert -delay 1x160 -loop 0 `ls *.png` `ls *.png|sort -r` FontForgeHOI.gif
