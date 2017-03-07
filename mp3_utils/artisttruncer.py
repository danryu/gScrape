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
                
            # fix duff artist <!-
            if 'artist' in entry:
                if entry['artist'] == "<!-":
                    print (show['showdate'])
                    print (entry['artist'])
                    print ("removing duff entry from show: " + show['showdate'])
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

with open("artisttruncd.json", "w") as outfile:
     json.dump(totaltrax, outfile, indent=2, sort_keys=True)            

