#!/usr/bin/env python3
"""Fetches freely licensed aircraft photos from Wikimedia Commons with author, licence and source.
Only CC BY, CC BY-SA, CC0 and public-domain files are kept."""
import json, os, re, time, html, urllib.parse, urllib.request
OUT = os.path.expanduser("~/Documents/aircraft-encyclopedia-media")
UA = "AircraftEncyclopediaApp/0.1 (photo credits kept; contact via app owner)"
AIRCRAFT = {
    "a350-900": ["Airbus A350-900", "Airbus A350-941"],
    "787-9": ["Boeing 787-9", "Boeing 787-9 Dreamliner"],
    "a380-800": ["Airbus A380-800", "Airbus A380-861"],
    "a320neo": ["Airbus A320neo", "Airbus A320-251N"],
    "g650er": ["Gulfstream G650ER", "Gulfstream G650"],
    "global-7500": ["Bombardier Global 7500"],
    "phenom-300e": ["Embraer Phenom 300E", "Embraer Phenom 300"],
    "falcon-8x": ["Dassault Falcon 8X"],
    "f-35a": ["F-35A Lightning II", "Lockheed Martin F-35A"],
    "typhoon": ["Eurofighter Typhoon FGR4", "Eurofighter Typhoon"],
    "c-130j": ["C-130J Super Hercules", "Lockheed Martin C-130J"],
    "a400m": ["Airbus A400M Atlas", "Airbus A400M"],
}
OK_LIC = re.compile(r"^(CC BY(-SA)? [0-9.]+|CC0|Public domain|PD.*)$", re.I)
PER = 6
def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)
def clean(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()
def main():
    os.makedirs(os.path.join(OUT, "photos"), exist_ok=True)
    media, report = {}, []
    for aid, queries in AIRCRAFT.items():
        picked, seen = [], set()
        for q in queries:
            if len(picked) >= PER: break
            try:
                d = api({"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
                         "gsrlimit": 30, "gsrsearch": f'"{q}" filetype:bitmap -cockpit -cabin',
                         "prop": "imageinfo", "iiprop": "url|extmetadata|size|mime", "iiurlwidth": 1280})
            except Exception as e:
                report.append(f"{aid}: search failed for {q}: {e}"); continue
            pages = sorted((d.get("query", {}).get("pages", {}) or {}).values(), key=lambda p: p.get("index", 999))
            for p in pages:
                if len(picked) >= PER: break
                ii = (p.get("imageinfo") or [{}])[0]
                em = ii.get("extmetadata", {})
                lic = clean(em.get("LicenseShortName", {}).get("value", ""))
                title = p.get("title", "")
                if title in seen or ii.get("mime") != "image/jpeg" or ii.get("width", 0) < 1400: continue
                if ii.get("width", 0) < ii.get("height", 0) or not OK_LIC.match(lic) or not ii.get("thumburl"): continue
                seen.add(title)
                n = len(picked) + 1
                fn = f"photos/{aid}-{n}.jpg"
                try:
                    req = urllib.request.Request(ii["thumburl"], headers={"User-Agent": UA})
                    with urllib.request.urlopen(req, timeout=60) as r, open(os.path.join(OUT, fn), "wb") as f:
                        f.write(r.read())
                except Exception as e:
                    report.append(f"{aid}: download failed {title}: {e}"); continue
                if os.path.getsize(os.path.join(OUT, fn)) < 20000:
                    os.remove(os.path.join(OUT, fn)); continue
                picked.append({"src": fn, "caption": clean(title.replace("File:", "").rsplit(".", 1)[0])[:90],
                               "credit": clean(em.get("Artist", {}).get("value", ""))[:80] or "Unknown author",
                               "licence": lic, "source": ii.get("descriptionurl", ""), "title": title})
                time.sleep(0.5)
        media[aid] = {"photos": picked}
        report.append(f"{aid}: {len(picked)} photos")
    with open(os.path.join(OUT, "media.json"), "w") as f:
        json.dump(media, f, indent=1, ensure_ascii=False)
    print("\n".join(report)); print("saved to", OUT)
main()
