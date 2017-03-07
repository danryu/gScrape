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

            # fix mistaken label - eg 2003-12-04
            # "blurb" : "(Genuine)" 
            # in this case set this blurb to be the label of preceding track. if label already set then either append or set to extrainfo
            indexnow = entry['index']
#            print ("INDEXNOW :%s" % indexnow)
            if 'artist' in entry and 'label' not in entry:
#                print (entry)
                emptylabelidx = entry['index']
                print (show['showdate'])
#                print ("INDEX: %s" % emptylabelidx)
#                print (" TRACK: %s" % entry)
#                print (" STRACK: %s" % showtrax[emptylabelidx-1])
#                if entry != showtrax[emptylabelidx-1]:
#                    print ("WHAAAAAAAAAAAAAT??")
                # TEST to see if there's a (label) blurb in the next entry
                if emptylabelidx < len(showtrax) - 1:

                    print (" TRACK: %s" % showtrax[emptylabelidx])
                    print (" LABEL: %s" % showtrax[emptylabelidx + 1])
                for nxentry in showtrax:
                    if nxentry['index'] == emptylabelidx + 1 and 'blurb' in nxentry:
                        b = re.match("^\(.*\)$", nxentry['blurb'])
                        if b is not None: # there is a label blurb so attach it to the label-free track previous
#                            pprint (show['showdate'])
#                            pprint ("TRACK: %s " % entry)
#                            pprint ("LABEL: " + nxentry['blurb'])                            
                            entry['label'] = nxentry['blurb']
                            copytrax.append(entry)
                            pprint ("FIXED ENTRY : %s" % entry)
                        else: # we didn't catch a label, never mind, just add the track entry as it is
                            copytrax.append(entry)
                            pprint ("WEIRD ENTRY : %s" % entry)
            elif 'blurb' in entry:
                b = re.match("^\(.*\)$", entry['blurb']) # lose the dangling (label) blurbs
                if b is not None:
                    pprint ("NOT ADDING : %s" % entry['blurb'])
                else:
                    copytrax.append(entry)
            else:
                copytrax.append(entry)
                pprint ("ADDING ENTRY :%s" % entry)
                
            # fix duff artist <!-
#            if 'artist' in entry:
#                if entry['artist'] == "<!-":
#                    print (show['showdate'])
#                    print (entry['artist'])
#                    print ("removing duff entry from show: " + show['showdate'])
#                    showtrax.remove(entry)

        shotraxlen = len(show['showtrax'])
        copytraxlen = len(copytrax)
        show['showtrax'] = copytrax
        if donething == True:
#            pprint (copytrax)
            print (show['showname'])
            print (" SHOWTRAX LENGTH: ", shotraxlen)
            print (" COPYTRAX LENGTH: ", copytraxlen)

with open("labelfixed.json", "w") as outfile:
     json.dump(totaltrax, outfile, indent=2, sort_keys=True)            

