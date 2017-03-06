# -*- coding: utf-8 -*-
import json
import re
import sys
import mutagen
from pprint import pprint
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

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
                print ("INDEX: %s" % emptylabelidx)
                print (" TRACK: %s" % entry)
                print (" STRACK: %s" % showtrax[emptylabelidx-1])
                if entry != showtrax[emptylabelidx-1]:
                    print ("WHAAAAAAAAAAAAAT??")
                # TEST to see if there's a (label) blurb in the next entry
#                if emptylabelidx < len(showtrax) - 1:

#                    print (" TRACK: %s" % showtrax[emptylabelidx])
#                    print (" LABEL: %s" % showtrax[emptylabelidx + 1])
#                for nxentry in showtrax:
#                    if nxentry['index'] == emptylabelidx + 1 and 'blurb' in nxentry:
#                        b = re.match("^\(.*\)$", nxentry['blurb'])
#                        if b is not None: # there is a label blurb so attach it to the label-free track previous
##                            pprint (show['showdate'])
##                            pprint ("TRACK: %s " % entry)
##                            pprint ("LABEL: " + nxentry['blurb'])                            
#                            entry['label'] = nxentry['blurb']
#                            copytrax.append(entry)
#                            pprint ("FIXED ENTRY : %s" % entry)
#                        else: # we didn't catch a label, never mind, just add the track entry as it is
#                            copytrax.append(entry)
#                            pprint ("WEIRD ENTRY : %s" % entry)
#            elif 'blurb' in entry:
#                    b = re.match("^\(.*\)$", entry['blurb']) # lose the dangling (label) blurbs
#                    if b is not None:
#                        pprint ("NOT ADDING : %s" % entry['blurb'])
#            else:
#                copytrax.append(entry)
#                pprint ("ADDING ENTRY :%s" % entry)
                
            # fix duff artist <!-
#            if 'artist' in entry:
#                if entry['artist'] == "<!-":
#                    print (show['showdate'])
#                    print (entry['artist'])
#                    print ("removing duff entry from show: " + show['showdate'])
#                    showtrax.remove(entry)
#    
            # fix these:
    #         "blurb": "<!-- All Comments -->",
    #         "trackname": "Untitled<!-- end IPS 2.52 pgid:126210-->"
    #         "blurb": "<u>",
#            if 'blurb' in entry:
#                b = re.match("<.*>", entry['blurb'])
#                if b is not None:
#                    print ("PRE-BLURB :" + entry['blurb'])      
#                    entry['blurb'] = re.sub(r'<.*?>', "", entry['blurb'])
#                    print ("POST-BLURB :" + entry['blurb'])

            # FIX THESE
#            "blurb": "00:00",#  "blurb": "2",# "blurb": "0200", "blurb": "01:00",
#            "blurb": "",
#            "blurb": "am",
#            "blurb": "Sorry we didn't ask for comments on this show.",
#            if 'blurb' in entry:
##                b = re.match("0?.[:.]?00$", entry['blurb'])
##                if b is not None:
##                if entry['blurb'] == "am":
##                if entry['blurb'] == "":
##                if entry['blurb'] == "Sorry we didn't ask for comments on this show.":
##                b = re.match("^.$", entry['blurb'])
##                if b is not None:
#                b = re.match("^\(.*\)$", entry['blurb'])
#                if b is not None:
#                    print ("PRINT BLURB: " + entry['blurb'])
#                    donething = True
#                    previous = entry['index'] - 1
#                    print ("CURRINDEX: ", entry['index'])
#                    print ("PREVINDEX: ",  previous)
#                    print("PREVENTRY: ", entry['previous'] )
#                else:
#                    copytrax.append(entry)
##                    print (entry)
#            else:
#                copytrax.append(entry)
#                print (entry)

        shotraxlen = len(show['showtrax'])
        copytraxlen = len(copytrax)
        show['showtrax'] = copytrax
        if donething == True:
#            pprint (copytrax)
            print (show['showname'])
            print (" SHOWTRAX LENGTH: ", shotraxlen)
            print (" COPYTRAX LENGTH: ", copytraxlen)

            ## remove \t everywhere
#            for key in entry:
##                print (key)
##                print (entry[key])
#                if key != "index" and entry[key] is not None:
#                    b = re.match(".*\t.*", entry[key])
#                    if b is not None:
#                        print ("PRE-BLURB :" + entry[key])      
#                        entry[key] = entry[key].replace("\t", ' ')
#                        print ("POST-BLURB :" + entry[key])


#             fix real tracks .... then entry.pop('blurb', None)
#             "blurb" : "Cannonball Adderley 'Tensity' (EMI)",
#             "blurb" : "7. The Detroit Experiment  ‘  Think Twice’  (Rope A Dope)"
#             "blurb" : "Julio Gutierrez\t-'Funk City'\t\t\t\t(Vico Records)",
#             "blurb" : "Sun Ra ­ 'Door of the Cosmos' (The Stars Are Singing, Singing Too) (Build An Ark Re Work) (Kindred Spirits)" ­
#             "blurb" : "Little Brother ­ 'Make Me Hot' (Yam Who Re Edit) (White)"
#             "blurb" : "Ryo Fukui ‘Early Summer’ (Trio)",
#             "blurb" : "Neil Ardley \"Will You Walk A Little Fatster?\" (EMI)"

#            if 'blurb' in entry:
#                print ("RAWPRE: " + entry['blurb'])
##                m = re.match("(.*)[\'‘](.*)[\'‘](\(.*\))$", entry['blurb'])
#                m = re.match("^(.*?)\s*([\"\'‘¹].*[\"\'’¹].*)(\(.*\))$", entry['blurb'])
#                if m is not None:
#                    print ("PRE: " + entry['blurb'])
#                    artist = m.group(1).strip("[-–­ ]")
#                    trackname = m.group(2).strip("[\"\'‘’]")
#                    label = m.group(3)
#                    # fix for double bracket pairs
#                    l = re.match("(\(.*\))\s*(\(.*\))", label)
#                    if l is not None:
#                        label = l.group(2)
#                        trackname = trackname + " " + l.group(1)
#                    # clean
#                    trackname = trackname.strip('\"\'‘’ -')
#                    label = label.strip("\(\)")
#                    print (" POST: artist: " + artist)
#                    print (" POST: trackname: " + trackname)
#                    print (" POST: label: " + label)
#                    entry['trackname'] = trackname
#                    entry['artist'] = artist
#                    entry['label'] = label
#                    entry.pop('blurb', None)
            
#            Irfane  Just A Little Lovin (White)
#            
#            \u2019 -> "\'"
#            \u2026 -> " "
#            \u00a0 -> " "
#            +++++++++++++++++++++++

#with open("mega_tagfix11.json", "w") as outfile:
#     json.dump(totaltrax, outfile, indent=2, sort_keys=True)            

