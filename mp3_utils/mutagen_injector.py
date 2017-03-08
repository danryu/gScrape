# -*- coding: utf-8 -*-
import json
import sys
import os
import re
from pprint import pprint
import urllib.request
import http.client, urllib.parse
import shutil
#import requests
#from requests_toolbelt.multipart.encoder import MultipartEncoder
from mixcloud import Mixcloud
#from mutagen.mp3 import MP3
#from mutagen.id3 import ID3

mp3files = sys.argv
mp3files.remove(mp3files[0])

# load the json trax into totaltrax
files = {'ultimate_mega_index.json'}
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
    