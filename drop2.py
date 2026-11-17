#!/usr/bin/env python3
"""Remove an unsuitable second photo.  Usage: python3 drop2.py id1 id2 ..."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(HERE, "batch4")
mpath = os.path.join(B, "media.json"); media = json.load(open(mpath))
for i in sys.argv[1:]:
    ph = media[i]["photos"]
    if len(ph) > 1:
        p = os.path.join(B, ph[1]["src"]); media[i]["photos"] = ph[:1]
        if os.path.exists(p): os.remove(p)
        print("dropped", i)
json.dump(media, open(mpath, "w"), indent=1)
