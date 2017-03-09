# -*- coding: utf-8 -*-
import json
import sys
import os
import re
from pprint import pprint
import urllib.request
import http.client, urllib.parse
import shutil
import requests
#from requests_toolbelt.multipart.encoder import MultipartEncoder

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

# here we load *.mp3
for mp3file in mp3files:
    filename = os.path.basename(mp3file)
    pprint (">>>>>>>>>>>>>> STARTING PROCESSING OF FILE: %s" % filename)
    d = re.match("^.*(20..)-([0-9]{2})-([0-9]{2}).*mp3$", filename)
    if d is not None:
        year = d.group(1)
        month = d.group(2)
        day = d.group(3)
        showdate = year + "-" + month + "-" + day
        print (showdate)
        for show in totaltrax:
            if 'showdate' in show:
                if show['showdate'] == showdate:
                    pprint (show['showdate'])
                    #    imgfile = downloadImgToFile()
                    imgfile = None
                    if 'showimgurl' in show:
                        imgurl = show['showimgurl']
                    else: 
                        imgurl = 'http://www.soulsessionsradio.com/wp-content/uploads/Gilles-Peterson.jpeg' #lol
                    print ("GONNA DOWNLOAD: " + imgurl)
                    with urllib.request.urlopen(imgurl) as response:
                        pprint (response.status)
                        imgfile = response.read()
#                    with open("/Users/dang/gilles_ichef/" + date + ".jpg", 'wb') as out_file:
#                        pprint (response.status)
#                        shutil.copyfileobj(response, out_file)
#                        pprint ("WHAT")
                    showdesc = None
                    if 'showdesc' in show:
                        showdesc  = show['showdesc']
                    showname = show['showname']
#                    params = urllib.parse.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
#                    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
#                    url = 'https://api.mixcloud.com/upload/?access_token=Yv6WrXJAxZXW3nMcEJNyU3aNNtax6gm6'
#                    files = {'file': ({'mp3': '@mp3file'},
#                                      {'description': showdesc},
#                                      {'name': showname})}                                      
#                    m = MultipartEncoder(
#                        fields={
#                                'mp3'           : mp3file,
#                                'description'   : showdesc,
#                                'name'          : showname,
#                               }
#                    )
#                    r = requests.post('https://api.mixcloud.com/upload/?access_token=Yv6WrXJAxZXW3nMcEJNyU3aNNtax6gm6', data=m, headers={'Content-Type': m.content_type})
                    payload = {'name' : "Gilles Peterson - Worldwide: " + showname + " - (" + showdate + ")" }
                    if showdesc is not None:
                        payload['description'] = showdesc

                    key_trax = [k['artist'] for k in show['showtrax'] if k.get('trackname')]
                    traxcount = len(key_trax)
                    show_length = ((2*60*60)-30)
                    avg_trac_len =  show_length / traxcount
                            
                    for entry in show['showtrax']:
                        idx = entry['index']
                        if 'artist' in entry: # it's a track
                            if 'label' in entry:
                                if entry['artist'] is not None and entry['label'] is not None:
                                    artist = entry['artist'] + " (" + entry['label'] + ")"
                            else:
                                artist = entry['artist']
                            payload['sections-%d-artist' % idx] = artist
                            payload['sections-%d-song' % idx] = entry['trackname']
                            # do VERY ROUGH tracktimes by averaging : showlength / number of tracks
                            # assume 20 seconds to get going and no trailers or news mid-show
                            payload['sections-%d-start_time' % idx] = 30+((idx-1)*avg_trac_len)    
                        elif 'blurb' in entry: # it's a blurb or title
                            payload['sections-%d-chapter' % idx] = entry['blurb']
                        elif 'title' in entry:
                            payload['sections-%d-chapter' % idx] = entry['title']
                    tags = ['soul', 'gilles peterson', 'worldwide','electronica', 'jazz']                            
                    for num, tag in enumerate(tags):
                        payload['tags-%s-tag' % num] = tag
                    with open(mp3file, 'rb') as file_to_go:
                        files = {'mp3': file_to_go}
                        pprint (files)
                        if imgfile is not None:
                            files['picture'] = imgfile
                        upload_url = 'https://api.mixcloud.com/upload/'
                        pprint("GONNA UPLOAD : %s" % payload)
                        pprint("GONNA UPLOAD FILE: %s" % mp3file)
                        r = requests.post(upload_url,
                                          data=payload,
                                          params={'access_token': 'Yv6WrXJAxZXW3nMcEJNyU3aNNtax6gm6'},
                                          files=files,
                                          )
                        pprint (r.status_code)
                        if r.status_code == "200":
                            pprint("SUCCESSFULLY POSTED FILE: %s" % mp3file)
                        else:
                            pprint("OOOPS: SOMETHING WENT WRONG!!")
                            pprint(r.raise_for_status())
                            pprint(r.headers)
                            
                    

# got access token by doing GET to 
#https://www.mixcloud.com/oauth/access_token?client_id=QbMYUcaj3SEeEXJKKE&redirect_uri=http://localhost:8000&client_secret=MdQUcCfKeAJaD93HLyc3B2BN3AJEcpGF&code=cSh49aL3W7
# access token resulting: Yv6WrXJAxZXW3nMcEJNyU3aNNtax6gm6



# can upload all 2007, 2008, 2009, 2010, 2011, some 2012 - mark some of 2008-10 as 80k / mid-fi - OR NOT UPLOAD ??
# OK. Plan.
# Upload the bits of 2007, 2008, 2010, all 2011, some 2012 - that are NOT 80k and are pre R6!
# Upload the Late Junctions ...


# after 2012-03-28 the recordings need to edited .... !!
# maybe manually! for about 2m10-20s at roughly 0h30, 1h30, 2h30 ...
