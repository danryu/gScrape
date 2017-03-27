# -*- coding: utf-8 -*-

# peaktest

#import json
import sys
#import os
#import re
#import time
#from pprint import pprint
#import urllib.request
#import http.client, urllib.parse
#import shutil
#import requests
#import fileinput
import pymediainfo
from pymediainfo import MediaInfo
#from requests.packages.urllib3.util.retry import Retry
#from requests.adapters import HTTPAdapter

#from collections import Counter
import sox

mp3file = sys.argv
mp3file.remove(mp3files[0])

filestats = []
with open(mp3file) as mfile:
    filestats = sox.file_info.stat(mfile)