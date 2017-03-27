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
#from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from collections import Counter

mp3files = sys.argv
mp3files.remove(mp3files[0])

archive = []
r = requests.get("https://api.mixcloud.com/danryu/cloudcasts/?limit=100")
for mix in r.json()['data']:
    m = re.match(".*worldwide.*(20..-..-..).*/$", mix['key'])
    if m is not None:
        date = m.group(1)
        archive.append(date)
    p = re.match(".*ww.*(20..-..-..).*/$", mix['key'])
    if p is not None:
        date = p.group(1)
        archive.append(date)
#        print (date)
#        print (mix['key'])
    
while 'next' in r.json()['paging']:
    print ("GOING DEEP ON THIS")
    nextpage = (r.json()['paging']['next'])
    r = requests.get(nextpage)
    for mix in r.json()['data']:
        m = re.match(".*worldwide.*(20..-..-..).*/$", mix['key'])
        if m is not None:
            date = m.group(1)
            archive.append(date)
        p = re.match(".*ww.*(20..-..-..).*/$", mix['key'])
        if p is not None:
            date = p.group(1)
            archive.append(date)

print(archive)
print (len(archive))

for thing in archive:
    if thing == '2011-04-27':
        print ("Jamie xx")
    if thing == '2011-05-18':
        print ("Obenewa")
    if thing == '2015-06-06':
        print ("Other Jamie XX")