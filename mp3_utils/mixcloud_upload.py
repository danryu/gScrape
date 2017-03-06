# -*- coding: utf-8 -*-
import json
import sys
import os
import re
from pprint import pprint
#from mutagen.mp3 import MP3
#from mutagen.id3 import ID3

mp3files = sys.argv
mp3files.remove(mp3files[0])

# load the json trax into totaltrax
files = {'data.json'}
totaltrax = []
for file in files:
    print ("Loading JSON: " + file)
    with open(file) as nextfile:
        megatrax = json.load(nextfile)
        for show in megatrax:
            totaltrax.append(show)

# here we load *.mp3
for mp3file in mp3files:
    filename = os.path.basename(mp3file)
    d = re.match("^.*(20..)-([0-9]{2})-([0-9]{2}).*mp3$", filename)
    if d is not None:
        year = d.group(1)
        month = d.group(2)
        day = d.group(3)
        date = year + "-" + month + "-" + day
        print (date)
#    muta = mutagen.File(file)
##    print(muta.info.length)
#    meta = MP3(file)
##    print(meta.info)
#    id3 = ID3(file)
#    composer = id3.getall('TCOM')[0]
#    title = id3.getall('TIT2')[0]
#    album = id3.getall('TALB')[0]
#    comment = id3.getall('COMM')
#    print (composer, title, album)
    
        for show in totaltrax:
            if 'showdate' in show:
                if show['showdate'] == date:
                    pprint (show)
    
#    date = getDateFromFileName()
#    getShowData(date)
#    imgfile = downloadImgToFile()
#    uploadToMixCloud(file,title,desc,tracklist with markers,img)
#    if success:
#        write successlog to json

#mp3
#REQUIRED. The audio file to be uploaded. The file should not be larger than 524288000 bytes.
#name
#REQUIRED (if a track). The track section song title.
#picture
#A picture for the upload. The file should not be larger than 10485760 bytes.
#description
#A description for the upload. Maximum of 1000 characters.
#tags-X-tag
#Where X is a number 0-4, a tag name for the upload. Up to 5 tags can be provided.

#sections-X-artist
#REQUIRED (if a track). The track section artist name.
#sections-X-song
#REQUIRED (if a track). The track section song title.
#sections-X-chapter
#The name of a chapter section.
#sections-X-start_time

#            for track in show['showtrax']:
#                if 'artist' in track:
#                    if track['artist'] == 'Terri Walker':
#                        pprint (show['showdate'])            
#                        pprint (show['showname'])
##                        pprint (show['showurl'])
##                        pprint (show['showdate'])
##                        pprint (show['showdesc'])
#                        pprint (track)

# mixcloud upload: for each file, get showdata, download img, then mixcloud UL(file,title,desc,tracklist with markers,img


# got access token by doing GET to 
#https://www.mixcloud.com/oauth/access_token?client_id=QbMYUcaj3SEeEXJKKE&redirect_uri=http://localhost:8000&client_secret=MdQUcCfKeAJaD93HLyc3B2BN3AJEcpGF&code=cSh49aL3W7
# access token resulting: Yv6WrXJAxZXW3nMcEJNyU3aNNtax6gm6



# can upload all 2007, 2008, 2009, 2010, 2011, some 2012 - mark some of 2008-10 as 80k / mid-fi - OR NOT UPLOAD ??
# OK. Plan.
# Upload the bits of 2007, 2008, 2010, all 2011, some 2012 - that are NOT 80k and are pre R6!
# Upload the Late Junctions ...


# after 2012-03-28 the recordings need to edited .... !!
# maybe manually! for about 2m10-20s at roughly 0h30, 1h30, 2h30 ...
