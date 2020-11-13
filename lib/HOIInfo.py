import fontforge

import json

HOI_INFO_VERSION = "v0"
HOI_INFO_HEADER = "!!FRB FF HOIINFO {}\n".format(HOI_INFO_VERSION)

def from_comments(font):
    HOI = dict()

    for g in font.glyphs():
        if len(g.comment) == 0 or not g.comment.startswith(HOI_INFO_HEADER): continue

        hoi_info = json.loads(g.comment[len(HOI_INFO_HEADER):])

        HOI[g.glyphname] = hoi_info

    return HOI

def set_HOI_rbearing(font, HOIdict, which):
    for g in font.glyphs():
        if g.glyphname not in HOIdict: continue
        hi = HOIdict[g.glyphname]
        g.width = hi["{}_rbearing".format(which)]
