import sys

import math

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def quit(reason, code=1):
    eprint(reason)
    sys.exit(code)

def has_layers(font):
    L = [e for e in font.layers]
    return 'End state' in L and 'HOI paths' in L

coords = lambda p: (math.floor(p.x), math.floor(p.y))

def get_point(i, layer):
    acc = 0
    for c in layer:
        for p in c:
            if acc == i:
                return p
            acc += 1

def dist(x1, x2, y1, y2):
    return math.sqrt(((x1-x2)**2) + ((y1-y2)**2))
