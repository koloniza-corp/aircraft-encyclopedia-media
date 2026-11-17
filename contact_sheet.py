#!/usr/bin/env python3
"""Make contact sheets of batch4 thumbnails (24 per sheet, labelled) for a visual check."""
import json, os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "batch4"); OUT = os.path.join(B, "sheets"); os.makedirs(OUT, exist_ok=True)
media = json.load(open(os.path.join(B, "media.json")))
ids = [i for i in json.load(open(os.path.join(HERE, "missing.json"))) if i["id"] in media]
start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
end = int(sys.argv[2]) if len(sys.argv) > 2 else len(ids)
W, H, C = 300, 190, 6
for s in range(start, end, 24):
    chunk = ids[s:s+24]; rows = (len(chunk) + C - 1) // C
    sheet = Image.new("RGB", (W * C, (H + 22) * rows), "white"); d = ImageDraw.Draw(sheet)
    for k, a in enumerate(chunk):
        x, y = (k % C) * W, (k // C) * (H + 22)
        try:
            im = Image.open(os.path.join(B, media[a["id"]]["thumb"])); im.thumbnail((W - 4, H - 4)); sheet.paste(im, (x + 2, y + 2))
        except Exception as e: d.text((x + 5, y + 5), "ERR", fill="red")
        d.text((x + 4, y + H + 4), f"{s+k} {a['id']}", fill="black")
    p = os.path.join(OUT, f"sheet-{s:03d}.jpg"); sheet.save(p, quality=70); print(p)
