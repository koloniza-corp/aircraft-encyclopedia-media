#!/usr/bin/env python3
"""Download Wikipedia article wikitext for each aircraft (facts are extracted later; descriptions are written fresh)."""
import json, os, time, urllib.parse, urllib.request, urllib.error
OUT = os.path.expanduser("~/Documents/aircraft-encyclopedia-media/pages")
UA = "AircraftEncyclopediaApp/0.2 (fact extraction; contact via app owner)"
T = {
 "a350-900":"Airbus A350","787-9":"Boeing 787 Dreamliner","a380-800":"Airbus A380","a320neo":"Airbus A320neo family",
 "g650er":"Gulfstream G650","global-7500":"Bombardier Global 7500","phenom-300e":"Embraer Phenom 300","falcon-8x":"Dassault Falcon 7X",
 "f-35a":"Lockheed Martin F-35 Lightning II","typhoon":"Eurofighter Typhoon","c-130j":"Lockheed Martin C-130J Super Hercules","a400m":"Airbus A400M Atlas",
 "737-max-8":"Boeing 737 MAX","737-800":"Boeing 737 Next Generation","747-8i":"Boeing 747-8","777-300er":"Boeing 777","767-300er":"Boeing 767",
 "757-200":"Boeing 757","a321neo":"Airbus A321neo","a330-900":"Airbus A330neo","a220-300":"Airbus A220","a350-1000":"Airbus A350",
 "e195-e2":"Embraer E-Jet E2 family","atr72-600":"ATR 72","dash8-400":"De Havilland Canada Dash 8","c919":"Comac C919",
 "crj900":"Bombardier CRJ700 series","md-11":"McDonnell Douglas MD-11",
 "g700":"Gulfstream G700","g280":"Gulfstream G280","challenger-350":"Bombardier Challenger 300","global-6500":"Bombardier Global Express",
 "falcon-6x":"Dassault Falcon 6X","falcon-900lx":"Dassault Falcon 900","falcon-2000lxs":"Dassault Falcon 2000","praetor-600":"Embraer Praetor 600",
 "phenom-100ev":"Embraer Phenom 100","citation-latitude":"Cessna Citation Latitude","citation-longitude":"Cessna Citation Longitude",
 "citation-cj4":"Cessna CitationJet/M2","hondajet":"HondaJet","pc-24":"Pilatus PC-24","learjet-75":"Learjet 75","acj320neo":"Airbus Corporate Jets",
 "f-22a":"Lockheed Martin F-22 Raptor","f-16":"General Dynamics F-16 Fighting Falcon","fa-18ef":"Boeing F/A-18E/F Super Hornet","f-15ex":"Boeing F-15EX Eagle II",
 "rafale":"Dassault Rafale","gripen-e":"Saab JAS 39E/F Gripen","su-57":"Sukhoi Su-57","j-20":"Chengdu J-20","su-35":"Sukhoi Su-35","mig-29":"Mikoyan MiG-29",
 "a-10c":"Fairchild Republic A-10 Thunderbolt II","b-52h":"Boeing B-52 Stratofortress","c-17a":"Boeing C-17 Globemaster III","kc-46a":"Boeing KC-46 Pegasus",
 "p-8a":"Boeing P-8 Poseidon","a330-mrtt":"Airbus A330 MRTT"}
def get(title):
    q = urllib.parse.urlencode({"action":"parse","page":title,"prop":"wikitext","redirects":1,"format":"json","formatversion":2})
    req = urllib.request.Request("https://en.wikipedia.org/w/api.php?"+q, headers={"User-Agent":UA})
    with urllib.request.urlopen(req, timeout=40) as r: return json.load(r)
os.makedirs(OUT, exist_ok=True); rep=[]
for aid, title in T.items():
    if os.path.exists(os.path.join(OUT, aid+".json")):
        rep.append(f"{aid}\tkept"); continue
    for attempt in range(6):
        try:
            j = get(title); break
        except urllib.error.HTTPError as e:
            if e.code != 429: raise
            time.sleep(int(e.headers.get("Retry-After") or 20) + 5)
    try:
        p = j.get("parse", {})
        json.dump({"id":aid,"asked":title,"title":p.get("title"),"pageid":p.get("pageid"),
                   "source":"https://en.wikipedia.org/wiki/"+urllib.parse.quote((p.get("title") or title).replace(" ","_")),
                   "wikitext":p.get("wikitext","")}, open(os.path.join(OUT, aid+".json"),"w"))
        rep.append(f"{aid}\t{p.get('title')}\t{len(p.get('wikitext',''))}")
    except Exception as e:
        rep.append(f"{aid}\tERROR {e}")
    time.sleep(4)
open(os.path.join(OUT,"_report.txt"),"w").write("\n".join(rep)); print("\n".join(rep))
