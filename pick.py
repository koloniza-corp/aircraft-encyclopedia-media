#!/usr/bin/env python3
"""Apply chosen replacement photos.  Usage: python3 pick.py id:3,5 id2:0   (first number becomes photo 1 + thumbnail)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_photos_250 as F
B = F.OUT; PH = F.PH
cand = json.load(open(os.path.join(B, "cand", "cand.json")))
mpath = os.path.join(B, "media.json"); media = json.load(open(mpath))
for arg in sys.argv[1:]:
    i, nums = arg.split(":"); picks = [cand[i][int(n)] for n in nums.split(",")]
    photos = []
    for k, g in enumerate(picks, 1):
        fn = f"{i}-{k}.jpg"; F.save(g["url"], os.path.join(PH, fn), 1024, 80)
        photos.append({"src": "photos/" + fn, "caption": g["desc"] or todo_name if False else (g["desc"] or i), "credit": g["author"], "licence": g["lic"], "source": g["page"]})
    if len(picks) == 1 and os.path.exists(os.path.join(PH, f"{i}-2.jpg")): os.remove(os.path.join(PH, f"{i}-2.jpg"))
    F.save(picks[0]["url"], os.path.join(PH, f"thumb-{i}.jpg"), 400, 74)
    media[i] = {"photos": photos, "thumb": f"photos/thumb-{i}.jpg"}
    print("updated", i, len(photos))
json.dump(media, open(mpath, "w"), indent=1)
