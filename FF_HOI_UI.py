import fontforge

import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import math

from lib.util import *

def autoNameGlyphPoints(junk, glyph):
    if not has_layers(glyph.font): return
    begin_state = glyph.layers["Fore"]
    end_state = glyph.layers["End state"]
    hoi_paths = glyph.layers["HOI paths"]
    
    Locs = dict()

    acc = 0

    for c in begin_state:
        for i, p in enumerate(c):
            Locs[(math.floor(p.x), math.floor(p.y))] = {"contour": c, "idx": i, "total_idx": acc, "on": p.on_curve}
            acc += 1

    new_hoi = fontforge.layer()
    for i, c in enumerate(hoi_paths):
        for p in c: p.name=''
        new_hoi+=c
        start = c[0]
        l = (math.floor(start.x), math.floor(start.y))
        if l in Locs:
            info = Locs[l]
            new_hoi[i][0].name = str(info["total_idx"])

    glyph.layers["HOI paths"] = new_hoi

fontforge.registerMenuItem(autoNameGlyphPoints, None, None, "Glyph", None, "_Higher-Order Interpolation", "Attempt to automatically _name points")
