#!/usr/bin/env python3
"""Real, freely licensed photos for the 250 aircraft that have none yet.
For each aircraft: read its English Wikipedia article, take the article's photos from Wikimedia Commons,
keep only CC BY / CC BY-SA / CC0 / public-domain JPEGs, skip drawings, logos, maps and cockpit-only shots,
and save 2 photos (1024 px) plus a thumbnail (400 px) with author, licence and source.
Run:  python3 fetch_photos_250.py   (needs: pip install pillow)"""
import json, os, re, sys, time, html, io, urllib.parse, urllib.request, urllib.error
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("OUT_DIR", os.path.join(HERE, "batch4"))
PH = os.path.join(OUT, "photos"); os.makedirs(PH, exist_ok=True)
UA = "AircraftEncyclopediaApp/1.0 (aviation encyclopedia; photo credits kept; contact support@aircraftmarket.co.uk)"
OK_LIC = re.compile(r"^(CC BY(-SA)? [0-9.]+|CC0( 1\.0)?|Public domain|PD[- ].*|PD)$", re.I)
BAD = re.compile(r"(?<![a-z])(logo|diagram|drawing|3view|3-view|three-view|map|seal|insignia|badge|emblem|flag|roundel|cockpit|instrument panel|interior|cabin|seats?|graph|chart|patch|scale model|model|toy|render|cgi|svg|silhouette|schematic|cutaway|crash|wreck|wreckage|accident)(?![a-z])", re.I)
def get(url, binary=False, tries=8):
    for a in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                d = r.read(); return d if binary else json.loads(d)
        except urllib.error.HTTPError as e:
            if e.code in (429, 503): time.sleep(int(e.headers.get("Retry-After") or 20) + 5); continue
            raise
        except Exception:
            time.sleep(5)
    raise RuntimeError("failed " + url)
def wp(params):
    time.sleep(1); return get("https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": "2"}))
def commons(params):
    time.sleep(1); return get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": "2"}))
def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()
def candidates(title):
    j = wp({"action": "query", "titles": title, "prop": "pageimages|images", "piprop": "original", "imlimit": "60", "redirects": "1"})
    pg = (j.get("query", {}).get("pages") or [{}])[0]
    files = []
    main = (pg.get("original") or {}).get("source", "")
    if main: files.append("File:" + urllib.parse.unquote(main.rsplit("/", 1)[-1]).replace("_", " "))
    for im in pg.get("images", []) or []:
        t = im.get("title", "")
        if t not in files: files.append(t)
    return [f for f in files if re.search(r"\.(jpe?g)$", f, re.I) and not BAD.search(f)], pg.get("title", title)
def commons_search(q):
    j = commons({"action": "query", "list": "search", "srnamespace": "6", "srlimit": "40", "srsearch": q + " filetype:bitmap"})
    return [r["title"] for r in j.get("query", {}).get("search", []) if re.search(r"\.(jpe?g)$", r["title"], re.I) and not BAD.search(r["title"])]
def info(files):
    out = []
    for i in range(0, len(files), 20):
        j = commons({"action": "query", "titles": "|".join(files[i:i+20]), "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": "1024"})
        for p in j.get("query", {}).get("pages", []):
            ii = (p.get("imageinfo") or [{}])[0]; m = ii.get("extmetadata", {})
            lic = clean((m.get("LicenseShortName") or {}).get("value"))
            if not ii.get("thumburl") or ii.get("mime") != "image/jpeg" or not OK_LIC.match(lic or ""): continue
            if (ii.get("width") or 0) < 800 or (ii.get("height") or 0) < 450: continue
            if (ii.get("width") or 1) / max(1, ii.get("height") or 1) < 1.05: continue   # landscape photos only
            out.append({"title": p["title"], "url": ii["thumburl"], "page": ii.get("descriptionurl", ""), "lic": lic,
                        "author": clean((m.get("Artist") or {}).get("value"))[:80] or "Unknown",
                        "desc": clean((m.get("ImageDescription") or {}).get("value"))[:160]})
    return out
def save(url, path, w, q):
    im = Image.open(io.BytesIO(get(url, binary=True))).convert("RGB")
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(path, "JPEG", quality=q, optimize=True, progressive=True)
USED = set()
def main():
    todo = json.load(open(os.path.join(HERE, "missing.json")))
    mpath = os.path.join(OUT, "media.json")
    media = json.load(open(mpath)) if os.path.exists(mpath) else {}
    for v in media.values():
        for p in v.get("photos", []): USED.add("File:" + urllib.parse.unquote(p["source"].rsplit("File:", 1)[-1]).replace("_", " "))
    for n, a in enumerate(todo, 1):
        if a["id"] in media and media[a["id"]].get("photos"): continue
        try:
            files, title = candidates(a["wiki"] or a["name"])
            short = re.sub(r"\s*\(.*?\)|\s*\".*?\"", "", a["name"]).strip()
            found = commons_search(short)
            files = found[:25] + [f for f in files if f not in found][:20]
            good = [g for g in info(files) if g["title"] not in USED]
            # prefer files whose name mentions the aircraft's model words
            words = [w.lower() for w in re.findall(r"[A-Za-z0-9]+", a["name"]) if len(w) > 1]
            good.sort(key=lambda g: -sum(w in g["title"].lower() for w in words))
            photos = []
            for k, g in enumerate(good[:2], 1):
                USED.add(g["title"])
                fn = f"{a['id']}-{k}.jpg"; save(g["url"], os.path.join(PH, fn), 1024, 80)
                photos.append({"src": "photos/" + fn, "caption": g["desc"] or a["name"], "credit": g["author"], "licence": g["lic"], "source": g["page"]})
            if photos:
                save(good[0]["url"], os.path.join(PH, f"thumb-{a['id']}.jpg"), 400, 74)
                media[a["id"]] = {"photos": photos, "thumb": f"photos/thumb-{a['id']}.jpg"}
            print(f"[{n}/{len(todo)}] {a['id']}: {len(photos)} photo(s)", flush=True)
        except Exception as e:
            print(f"[{n}/{len(todo)}] {a['id']}: FAILED {e}", flush=True)
        json.dump(media, open(mpath, "w"), indent=1)
    miss = [a["id"] for a in todo if a["id"] not in media]
    print("done", len(media), "aircraft with photos;", len(miss), "without:", " ".join(miss))
if __name__ == "__main__": main()
