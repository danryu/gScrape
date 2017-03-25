# -*- coding: utf-8 -*-
import json
import sys
import os
import re
import time
from pprint import pprint
import urllib.request
import http.client, urllib.parse
import shutil
import requests
import fileinput
#import pymediainfo
#from pymediainfo import MediaInfo
#from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from collections import Counter

mp3files = sys.argv
mp3files.remove(mp3files[0])

# load the json trax index into totaltrax
files = {'ultimate_index_manfixd.json'}
totaltrax = []
for file in files:
    print ("Loading JSON: " + file)
    with open(file) as nextfile:
        megatrax = json.load(nextfile)
        for show in megatrax:
            totaltrax.append(show)
            
for show in totaltrax:
    if 'showdesc' in show:
        if len(show['showdesc']) > 834:
            print (show['showdate'])
            print (len(show['showdesc']))
