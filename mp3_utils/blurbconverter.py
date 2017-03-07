# -*- coding: utf-8 -*-
import json
import re
import sys
from pprint import pprint

files = sys.argv
files.remove(files[0])

totaltrax = []
for file in files:
    print (file)
    with open(file) as nextfile:
        megatrax = json.load(nextfile)
        for show in megatrax:
            totaltrax.append(show)

for show in totaltrax:
    copytrax = []
    donething = False

    if 'showtrax' in show:
        showtrax = show['showtrax']
        for entry in showtrax:
            # FIXES by section ... follow each section comments
#             fix real tracks .... then entry.pop('blurb', None)
#             "blurb" : "Cannonball Adderley 'Tensity' (EMI)",
#             "blurb" : "7. The Detroit Experiment  ‘  Think Twice’  (Rope A Dope)"
#             "blurb" : "Julio Gutierrez\t-'Funk City'\t\t\t\t(Vico Records)",
#             "blurb" : "Sun Ra ­ 'Door of the Cosmos' (The Stars Are Singing, Singing Too) (Build An Ark Re Work) (Kindred Spirits)" ­
#             "blurb" : "Little Brother ­ 'Make Me Hot' (Yam Who Re Edit) (White)"
#             "blurb" : "Ryo Fukui ‘Early Summer’ (Trio)",
#             "blurb" : "Neil Ardley \"Will You Walk A Little Fatster?\" (EMI)"

            if 'blurb' in entry:
                print ("RAWPRE: " + entry['blurb'])
#                m = re.match("(.*)[\'‘](.*)[\'‘](\(.*\))$", entry['blurb'])
                m = re.match("^(.*?)\s*([\"\'‘¹].*[\"\'’¹].*)(\(.*\))$", entry['blurb'])
                if m is not None:
                    print ("PRE: " + entry['blurb'])
                    artist = m.group(1).strip("[-–­ ]")
                    trackname = m.group(2).strip("[\"\'‘’]")
                    label = m.group(3)
                    # fix for double bracket pairs
                    l = re.match("(\(.*\))\s*(\(.*\))", label)
                    if l is not None:
                        label = l.group(2)
                        trackname = trackname + " " + l.group(1)
                    # clean
                    trackname = trackname.strip('\"\'‘’ -')
                    label = label.strip("\(\)")
                    print (" POST: artist: " + artist)
                    print (" POST: trackname: " + trackname)
                    print (" POST: label: " + label)
                    entry['trackname'] = trackname
                    entry['artist'] = artist
                    entry['label'] = label
                    entry.pop('blurb', None)
                    copytrax.append(entry)
                else:
                    copytrax.append(entry)
            else:
                copytrax.append(entry)

        shotraxlen = len(show['showtrax'])
        copytraxlen = len(copytrax)
        show['showtrax'] = copytrax
        if donething == True:
#            pprint (copytrax)
            print (show['showname'])
            print (" SHOWTRAX LENGTH: ", shotraxlen)
            print (" COPYTRAX LENGTH: ", copytraxlen)


#            Irfane  Just A Little Lovin (White)
#            
#            \u2019 -> "\'"
#            \u2026 -> " "
#            \u00a0 -> " "
#            +++++++++++++++++++++++

with open("blurbconverted.json", "w") as outfile:
     json.dump(totaltrax, outfile, indent=2, sort_keys=True)            

