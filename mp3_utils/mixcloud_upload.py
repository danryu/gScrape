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
import pymediainfo
from pymediainfo import MediaInfo
#from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from collections import Counter

mp3files = sys.argv
mp3files.remove(mp3files[0])

# LOAD JSON INDEX: load the json trax index into totaltrax
files = {'ultimate_index_manfixd.json'}
totaltrax = []
for file in files:
    print ("Loading JSON: " + file)
    with open(file) as nextfile:
        megatrax = json.load(nextfile)
        for show in megatrax:
            totaltrax.append(show)

# CHECK EXISTING ARCHIVE ONLINE
# get archive as it exists already - limit is 100 so cycle through 'next' pages
archive = []
r = requests.get("https://api.mixcloud.com/danryu/cloudcasts/?limit=100")
for mix in r.json()['data']:
    m = re.match(".*gilles.*(20..-..-..).*/$", mix['key'])
    if m is not None:
        date = m.group(1)
        archive.append(date)
    p = re.match(".*ww.*(20..-..-..).*/$", mix['key'])
    if p is not None:
        date = p.group(1)
        archive.append(date)
while 'next' in r.json()['paging']:
    print ("GOING DEEP ON THIS")
    nextpage = (r.json()['paging']['next'])
    r = requests.get(nextpage)
    for mix in r.json()['data']:
        m = re.match(".*gilles.*(20..-..-..).*/$", mix['key'])
        if m is not None:
            date = m.group(1)
            archive.append(date)
        p = re.match(".*ww.*(20..-..-..).*/$", mix['key'])
        if p is not None:
            date = p.group(1)
            archive.append(date)
for date in archive:
    print ("Worldwide show from %s already archived. Not uploading." % date)

# MAIN FILE UPLOAD LOOP
# here we load *.mp3
for mp3file in mp3files:
    media_info = MediaInfo.parse(mp3file)
    for track in media_info.tracks:
        if track.track_type == 'Audio':
            show_length = track.duration/1000
            print ("SHOWLENGTH: %s" % show_length)
    filename = os.path.basename(mp3file)
    print (">>>>>>>>>>>>>> STARTING PROCESSING OF FILE: %s" % filename)
    d = re.match("^.*(20..)-([0-9]{2})-([0-9]{2}).*mp3$", filename) #FIXME could do better match here - eg .*Gilles.*...
    if d is not None:
        year = d.group(1)
        month = d.group(2)
        day = d.group(3)
        showdate = year + "-" + month + "-" + day
        print ("DEBUG: showdate: %s" % showdate)
        if showdate in archive:
            print("DEBUG: show is already uploaded! Not doing date %s" % showdate)
        for show in totaltrax:
            if 'showdate' in show and showdate not in archive: # check it's not already uploaded
                if show['showdate'] == showdate: # json index entry matches the filename! MATCH!
                    pprint ("FOUND SHOW IN INDEX: %s" % show['showdate'])
                    #    imgfile = downloadImgToFile()
                    imgfile = None
                    if 'showimgurl' in show:
                        imgurl = show['showimgurl']
                    else: 
                        imgurl = 'http://www.soulsessionsradio.com/wp-content/uploads/Gilles-Peterson.jpeg' #lol
                    print ("GONNA DOWNLOAD IMG: " + imgurl)
                    with urllib.request.urlopen(imgurl) as response:
                        pprint ("IMG DL RESPONSE: %s " % response.status)
                        imgfile = response.read()

                    # WRITE PAYLOAD SECTIONS
                    # SECTION: write showname
                    showname = show['showname']
                    payload = {'name' : "Gilles Peterson - Worldwide: " + showname + " - (" + showdate + ")" }
                    if len(payload['name']) > 100:
                        payload['name'] = "GP WW: " + showname + " - (" + showdate + ")" 
                    
                    # SECTION: write showdesc
                    showdesc = None
                    if 'showdesc' in show:
                        showdesc  = show['showdesc']
                    if showdesc is not None:
                        showdesc = showdesc[:1000] # limit showdesc to 1000 characters for mixcloud
                        payload['description'] = showdesc
                    else:
                        payload['description'] = showname # use showname as backup description
                    # inject banner if we've got room - banner is 166 characters. only add if description will fit
                    banner_string = "-- WITH LOVE FOR THE MUSIC -- WITH THANKS TO GILLES AND THE ARTISTS --\\\n\
                    \\\nCHECK THE TRACKLISTINGS FOR FULL SESSION INFO\\\nBBC Summary:\\\n"
                    if len(payload['description']) < 864:
                        payload['description'] =  banner_string + payload['description']
                    print("DEBUG: descr length: %s" % len(payload['description']))
                    
                    # SECTION: write TRACKLISTINGS to payload
                    key_trax = [k['artist'] for k in show['showtrax'] if k.get('trackname')]
                    traxcount = len(key_trax)
                    print ("DEBUG: SHOW_LENGTH: %s" % show_length)
                    avg_trac_len =  int(round(show_length / traxcount))  # make this a round number
                    print ("DEBUG: AVG_TRAC_LEN: %s" % avg_trac_len)
                    trac_count = 0 # hacky counter to track the number of tracks ...                             
                    for entry in show['showtrax']:
                        idx = entry['index']
                        if 'artist' in entry: # it's a track
                            trac_count = trac_count + 1                            
                            # set artist 
                            artist = None
                            if 'label' in entry:
                                if entry['artist'] is not None and entry['label'] is not None: # add label to artist name
                                    artist = entry['artist'] + " (" + entry['label'] + ")"
                                elif entry['label'] is None: # in case label is entry but it's null
                                    artist = entry['artist']
                            else:
                                artist = entry['artist']
                            payload['sections-%d-artist' % idx] = artist
                            
                            # SET trackname tag
                            payload['sections-%d-song' % idx] = entry['trackname']
                            # do VERY ROUGH tracktimes by averaging : showlength / number of tracks
                            # assume 30 seconds to get going and no trailers or news mid-show
                            if trac_count > 1:
                                starttime = ((trac_count-1)*avg_trac_len) - 30
                                pprint ("DEBUG: IDX: %s - STARTTIME: %s" % (trac_count, starttime))
                            else:
                                starttime = ((trac_count-1)*avg_trac_len)  # always zero for sections-1-start_time I think
                                pprint ("DEBUG: IDX: %s - STARTTIME: %s" % (trac_count, starttime))
                            payload['sections-%d-start_time' % idx] = starttime
                        elif 'blurb' in entry: # it's a blurb
                            payload['sections-%d-chapter' % idx] = entry['blurb']
                        elif 'title' in entry: #  or title
                            payload['sections-%d-chapter' % idx] = entry['title']                    
                    # debug time
                    for k,v in payload.items():
                        print ("DEBUG: PAYLOAD KEY: %s, VAL: %s" % (k,v))                    
                    # fix for DMCA restriction in USA: http://support.mixcloud.com/customer/portal/articles/1590263-us-licensing-rules-for-uploaders
                    # for every artist with over 3 occurrences in tracklist, count the number of tracks with this artist
                    artist_count = Counter(payload.values())
                    for ct_artist, count in artist_count.items():
                        if count > 3 and ct_artist is not None: #  catch for null artist
                            pprint("DEBUG COUNT: %s ARTIST: %s" % (count, ct_artist))
                            # now go though whole list and substitute "." chars to artistname after 3rd occurrence
                            surplus = 0
                            for k, v in payload.items():
                                if v == ct_artist:
                                    pprint (k + ":" + v)
                                    surplus = surplus + 1
                                    if surplus > 3:
                                        extrachars = surplus - 3 # this is no of extra chars we have to append
                                        prestring = ""
                                        for x in range(0, extrachars):
                                            prestring = "." + prestring
#                                            pprint ("DEBUG: PRESTRING NOW: %s" % prestring)
                                        newartist = prestring + ct_artist
                                        pprint ("DEBUG: ARTIST NOW: %s" % newartist)
                                        payload[k] = newartist
                    
                    # SECTION: write tags
                    tags = ['soul', 'gilles peterson', 'worldwide','electronica', 'jazz']                            
                    for num, tag in enumerate(tags):
                        payload['tags-%s-tag' % num] = tag

                    # PREPARE file to upload
                    with open(mp3file, 'rb') as file_to_go:
                        files = {'mp3': file_to_go}
                        if imgfile is not None:
                            files['picture'] = imgfile
                        upload_url = 'https://api.mixcloud.com/upload/'
#                        pprint("GONNA UPLOAD PAYLOAD: %s" % payload)
                        print("GONNA UPLOAD FILE: %s" % mp3file)
                        s = requests.Session()
                        retries = Retry(total=5,
                                        backoff_factor=20,
                                        status_forcelist=[ 400, 401, 402, 403, 500, 502, 503, 504 ])
                        s.mount('http://', HTTPAdapter(max_retries=retries))
                        r = s.post(upload_url,
                              data=payload,
                              params={'access_token': 'Yv6WrXJAxZXW3nMcEJNyU3aNNtax6gm6'},
                              files=files,
                              )
                        print ("UPLOAD STATUS CODE: %s" % r.status_code)
                        if r.status_code == 200:
                            print("SUCCESSFULLY POSTED FILE: %s" % mp3file)
                            pprint("RESPONSE TEXT: %s" % r.json() )
                            if r.json()['result']['success'] == True:
                                pprint("FILE DONE! %s" % mp3file)
                        else:
                            pprint ("STATUS CODE: %s" % r.status_code)
                            print("OOOPS: SOMETHING WENT WRONG!!")
                            pprint("RESPONSE TEXT: %s" % r.json())
                            if r.json()['error']['type'] == "RateLimitException":
                                pprint("RATE LIMIT EXCEPTION.. BACK OFF FOR: %s" % r.json()['error']['retry_after'])
                            pprint(r.raise_for_status())
                            pprint(r.headers)
                    
                    # cool off now for a few seconds before attempting the next upload
                    print("DEBUG: SLEEPING NOW FOR 20 SECONDS .... ")
                    time.sleep(20)

# MIXCLOUD API DOCS:
#curl -F mp3=@upload.mp3 \
#     -F "name=API Upload" \
#     -F "tags-0-tag=Test" \
#     -F "tags-1-tag=API" \
#     -F "sections-0-chapter=Introduction" \
#     -F "sections-0-start_time=0" \
#     -F "sections-1-artist=Artist Name" \
#     -F "sections-1-song=Song Title" \
#     -F "sections-1-start_time=10" \
#     -F "description=My test upload" \
#     https://api.mixcloud.com/upload/?access_token=INSERT_ACCESS_TOKEN_HERE                    

# ACCESS TOKEN
# got access token by doing GET to 
#https://www.mixcloud.com/oauth/access_token?client_id=QbMYUcaj3SEeEXJKKE&redirect_uri=http://localhost:8000&client_secret=MdQUcCfKeAJaD93HLyc3B2BN3AJEcpGF&code=cSh49aL3W7
# access token resulting: Yv6WrXJAxZXW3nMcEJNyU3aNNtax6gm6


