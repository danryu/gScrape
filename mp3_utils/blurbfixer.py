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
            
            ## remove \t everywhere
            for key in entry:
#                print (key)
#                print (entry[key])
                if key != "index" and entry[key] is not None:
                    b = re.match(".*\t.*", entry[key])
                    if b is not None:
                        print ("PRE-BLURB :" + entry[key])      
                        entry[key] = entry[key].replace("\t", ' ')
                        print ("POST-BLURB :" + entry[key])
            
            # fix these:
    #         "blurb": "<!-- All Comments -->",
    #         "trackname": "Untitled<!-- end IPS 2.52 pgid:126210-->"
    #         "blurb": "<u>",
            if 'blurb' in entry:
                b = re.match("<.*>", entry['blurb'])
                if b is not None:
                    print ("PRE-BLURB :" + entry['blurb'])      
                    entry['blurb'] = re.sub(r'<.*?>', "", entry['blurb'])
                    print ("POST-BLURB :" + entry['blurb'])

            # FIX THESE
#            "blurb": "00:00",#  "blurb": "2",# "blurb": "0200", "blurb": "01:00",
#            "blurb": "",
#            "blurb": "am",
#            "blurb": "Sorry we didn't ask for comments on this show.",
            if 'blurb' in entry:
                b = re.match("0?.[:.]?00$", entry['blurb'])
#                if b is not None:
#                if entry['blurb'] == "am":
#                if entry['blurb'] == "":
#                if entry['blurb'] == "Sorry we didn't ask for comments on this show.":
                c = re.match("^.$", entry['blurb'])
#                if c is not None:
                d = re.match("^\++$", entry['blurb'])
                e = re.match("^Your\s+comments on the tracks$", entry['blurb'])
                if b is not None or c is not None or d is not None or e is not None or entry['blurb'] == "am" or entry['blurb'] == "" or entry['blurb'] == "Sorry we didn't ask for comments on this show.":
                    print ("DO NOTHING WITH :" + entry['blurb'])
                else:
                    copytrax.append(entry)
#                    print (entry)
            else:
                copytrax.append(entry)
                print (entry)

        shotraxlen = len(show['showtrax'])
        copytraxlen = len(copytrax)
        show['showtrax'] = copytrax
        if donething == True:
#            pprint (copytrax)
            print (show['showname'])
            print (" SHOWTRAX LENGTH: ", shotraxlen)
            print (" COPYTRAX LENGTH: ", copytraxlen)


with open("blurbfixed.json", "w") as outfile:
     json.dump(totaltrax, outfile, indent=2, sort_keys=True)            

