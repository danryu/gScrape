# -*- coding: utf-8 -*-
import json
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

#for show in totaltrax:
#    if 'showdate' in show:
#        pprint (show['showdate'])

with open("merged_file.json", "w") as outfile:
     json.dump(totaltrax, outfile, indent=2, sort_keys=True)