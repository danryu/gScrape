# -*- coding: utf-8 -*-
import json
import sys
import mutagen
from pprint import pprint
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

files = sys.argv
files.remove(files[0])

#totaltrax = []
#for file in files:
#    print (file)
#    with open(file) as nextfile:
#        megatrax = json.load(nextfile)
#        for show in megatrax:
#            totaltrax.append(show)
#
#for show in totaltrax:
#    if 'showdate' in show:
#        pprint (show['showdate'])


for file in files:
    print (file)
    muta = mutagen.File(file)
    print(muta.info.length)
    meta = MP3(file)
    print(meta.info)
    id3 = ID3(file)
    composer = id3.getall('TCOM')[0]
    title = id3.getall('TIT2')[0]
    album = id3.getall('TALB')[0]
    comment = id3.getall('COMM')
    print (composer, title, album)
#    print(id3.getall('TCOM')[0])
#    print(id3.getall('TIT2')[0])
#    print(id3.getall('TALB')[0])
        
        
#            for track in show['showtrax']:
#                if 'artist' in track:
#                    if track['artist'] == 'Terri Walker':
#                        pprint (show['showdate'])            
#                        pprint (show['showname'])
##                        pprint (show['showurl'])
##                        pprint (show['showdate'])
##                        pprint (show['showdesc'])
#                        pprint (track)


#with open("merged_file.json", "w") as outfile:
#     json.dump(totaltrax, outfile)

