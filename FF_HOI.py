#!/usr/bin/env python3
import fontforge

import argparse
import itertools
import os
import shutil

from lib.util import *
# This handles the glyph's "HOIINFO" comment. Right now only deals with setting rbearing of each master.
from lib import HOIInfo

parser = argparse.ArgumentParser(description='Given a specially formatted input SFD, output UFO files suitable for non-linear OpenType Font Variations, buildable with Fontmake and TTX.')
parser.add_argument('SFD', type=str)
args = parser.parse_args()

eprint("Performing sanity check on font: {} …".format(args.SFD))

font = fontforge.open(args.SFD)
HOIdict = HOIInfo.from_comments(font)

# Sanity tests

if not has_layers(font):
    exit("SFD does not have required layers; read documentation.")

assert all([not font.layers[l].is_quadratic for l in font.layers]), "Only cubic layers supported in this version"

for g in font.glyphs():
    eprint("Checking sanity of glyph: {} …".format(g.glyphname))
    for c in g.layers["HOI paths"]:
        assert c[0].name.isdigit(), "HOI path not integer name"
        assert coords(c[0]) in [coords(p) for p in c], "Misaligned HOI path"

eprint("Sane (🤞). Beginning UFO generation …")
eprint("Generating master: A")

def reset_ufo(which, font):
    ufo = font.fullname+"-{}.ufo".format(which)
    if os.path.exists(ufo) and os.path.isdir(ufo):
        shutil.rmtree(ufo)
    font.generate(ufo, flags=("opentype", "no-hints", "omit-instructions"))
    font.close()

def del_unneeded_ufo_layers(font):
    for l in font.layers:
        if l != "Fore" and l != "Back":
            del font.layers[l]

HOIInfo.set_HOI_rbearing(font, HOIdict, "c1")
del_unneeded_ufo_layers(font)
reset_ufo("A", font)

eprint("Generating master: B")
font = fontforge.open(args.SFD)

def make_master(g, d1, d2):
    deltas = dict()

    for c in g.layers["HOI paths"]:
        dx = c[d1].x - c[d2].x
        dy = c[d1].y - c[d2].y
        deltas[int(c[0].name)] = {"dx": dx, "dy": dy}

    newfore = fontforge.layer()

    acc = 0
    for i, c in enumerate(g.foreground):
        for j, p in enumerate(c):
            if acc in deltas:
                p.x += deltas[acc]["dx"]
                p.y += deltas[acc]["dy"]
            acc+=1
        newfore+=c

    pts_s = list(itertools.chain.from_iterable(g.foreground))
    pts_e = list(itertools.chain.from_iterable(g.layers["End state"]))

    deltas2 = dict()

    for i, pt in enumerate(pts_s):
        if i in deltas: continue
        lpt = pts_e[i]
        if pt.x == lpt.x and pt.y == lpt.y: continue
        if i-1 in deltas and pts_s[i-1].on_curve:
            deltas2[i] = deltas[i-1]
        elif i+1 in deltas and pts_s[i+1].on_curve:
            deltas2[i] = deltas[i+1]
        elif i == len(pts_s)-1 and 0 in deltas:
            deltas2[i] = deltas[0]

    acc = 0
    for i, c in enumerate(newfore):
        for j, p in enumerate(c):
            if acc in deltas2:
                p.x += deltas2[acc]["dx"]
                p.y += deltas2[acc]["dy"]
            newfore[i][j] = p
            acc+=1

    g.foreground = newfore

for g in font.glyphs():
    eprint("Glyph: {}".format(g.glyphname))
    make_master(g, 1, 0)

HOIInfo.set_HOI_rbearing(font, HOIdict, "c2")
del_unneeded_ufo_layers(font)
reset_ufo("B", font)

eprint("Generating master: C")
font = fontforge.open(args.SFD)

for g in font.glyphs():
    eprint("Glyph: {}".format(g.glyphname))
    make_master(g, 2, 0)

HOIInfo.set_HOI_rbearing(font, HOIdict, "c3")
del_unneeded_ufo_layers(font)
reset_ufo("C", font)

eprint("Generating master: D")
font = fontforge.open(args.SFD)
for g in font.glyphs():
    g.foreground = g.layers["End state"]

del_unneeded_ufo_layers(font)
reset_ufo("D", font)

eprint("Done!")
