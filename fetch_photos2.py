#!/usr/bin/env python3
"""Second photo batch: 48 new aircraft, freely licensed Commons photos only, with credits."""
import importlib.util, os
spec = importlib.util.spec_from_file_location("fp", os.path.expanduser("~/Documents/aircraft-encyclopedia-media/fetch_photos_polite.py"))
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
m.OUT = os.path.expanduser("~/Documents/aircraft-encyclopedia-media/batch3"); m.PER = 6
m.AIRCRAFT = {
 "737-max-8":["Boeing 737 MAX 8","737-8"],"737-800":["Boeing 737-800","737-8AS"],"747-8i":["Boeing 747-8I","747-830"],
 "777-300er":["Boeing 777-300ER","777-31H(ER)"],"767-300er":["Boeing 767-300ER"],"757-200":["Boeing 757-200"],
 "a321neo":["Airbus A321neo","A321-271N"],"a330-900":["Airbus A330-900","A330-941"],"a220-300":["Airbus A220-300","A220-300"],
 "a350-1000":["Airbus A350-1000","A350-1041"],"e195-e2":["Embraer E195-E2","ERJ-190-400"],"atr72-600":["ATR 72-600","ATR 72-212A"],
 "dash8-400":["Dash 8-400","DHC-8-402"],"c919":["Comac C919"],"crj900":["Bombardier CRJ900","CRJ-900"],"md-11":["McDonnell Douglas MD-11"],
 "g700":["Gulfstream G700"],"g280":["Gulfstream G280"],"challenger-350":["Bombardier Challenger 350"],"global-6500":["Bombardier Global 6500","Global 6000"],
 "falcon-6x":["Dassault Falcon 6X"],"falcon-900lx":["Dassault Falcon 900LX","Falcon 900EX"],"falcon-2000lxs":["Dassault Falcon 2000LXS","Falcon 2000LX"],
 "praetor-600":["Embraer Praetor 600","Legacy 500"],"phenom-100ev":["Embraer Phenom 100"],"citation-latitude":["Cessna Citation Latitude"],
 "citation-longitude":["Cessna Citation Longitude"],"citation-cj4":["Cessna Citation CJ4","Citation CJ4"],"hondajet":["HondaJet","HA-420"],
 "pc-24":["Pilatus PC-24"],"learjet-75":["Learjet 75","Learjet 45"],"acj320neo":["ACJ320neo","Airbus ACJ320"],
 "f-22a":["F-22 Raptor","F-22A"],"f-16":["F-16 Fighting Falcon","F-16C"],"fa-18ef":["F/A-18E Super Hornet","F/A-18F Super Hornet"],
 "f-15ex":["F-15EX Eagle II","F-15EX"],"rafale":["Dassault Rafale"],"gripen-e":["Gripen E","JAS 39E"],"su-57":["Sukhoi Su-57"],
 "j-20":["Chengdu J-20"],"su-35":["Sukhoi Su-35S","Su-35"],"mig-29":["Mikoyan MiG-29","MiG-29"],"a-10c":["A-10C Thunderbolt II","A-10 Thunderbolt"],
 "b-52h":["B-52H Stratofortress","B-52H"],"c-17a":["C-17 Globemaster III","C-17A"],"kc-46a":["KC-46 Pegasus","KC-46A"],
 "p-8a":["P-8 Poseidon","P-8A"],"a330-mrtt":["A330 MRTT","Airbus A330 MRTT"]}
m.main()
