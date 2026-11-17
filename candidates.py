#!/usr/bin/env python3
"""For aircraft whose photo was wrong: list up to 8 alternative Commons photos, save small previews
and one labelled sheet per aircraft, plus cand.json so a choice can be applied with pick.py.
Usage: python3 candidates.py id1 id2 ...   (optional search text: id=Search words)"""
import json, os, sys, re, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fetch_photos_250 as F
from PIL import Image, ImageDraw
B = F.OUT; CD = os.path.join(B, "cand"); os.makedirs(CD, exist_ok=True)
todo = {a["id"]: a for a in json.load(open(os.path.join(F.HERE, "missing.json")))}
media = json.load(open(os.path.join(B, "media.json")))
used = set()
for v in media.values():
    for p in v.get("photos", []): used.add(p["source"])
cpath = os.path.join(CD, "cand.json"); cand = json.load(open(cpath)) if os.path.exists(cpath) else {}
for arg in sys.argv[1:]:
    i, _, q = arg.partition("="); a = todo[i]
    q = q or re.sub(r"\s*\(.*?\)|\s*\".*?\"", "", a["name"]).strip()
    files = F.commons_search(q)
    good = [g for g in F.info(files[:40]) if g["page"] not in used][:8]
    cand[i] = good
    sheet = Image.new("RGB", (4 * 300, 2 * 212), "white"); d = ImageDraw.Draw(sheet)
    for k, g in enumerate(good):
        try:
            im = Image.open(io.BytesIO(F.get(g["url"], binary=True))).convert("RGB"); im.thumbnail((296, 186))
            sheet.paste(im, ((k % 4) * 300 + 2, (k // 4) * 212 + 2))
        except Exception: pass
        d.text(((k % 4) * 300 + 4, (k // 4) * 212 + 192), f"{k}: {g['title'][5:45]}", fill="black")
    sheet.save(os.path.join(CD, f"{i}.jpg"), quality=72); print(i, len(good), flush=True)
    json.dump(cand, open(cpath, "w"), indent=1)
