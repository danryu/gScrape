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

date_dict  = {'01':'Jan',
              '02':'Feb',
              '03':'Mar',
              '04':'Apr',
              '05':'May',
              '06':'Jun',
              '07':'Jul',
              '08':'Aug',
              '09':'Sep',
              '10':'Oct',
              '11':'Nov',
              '12':'Dec'}

totaltrax = []
for file in files:
    print (file)
    with open(file) as nextfile:
        megatrax = json.load(nextfile)
        for show in megatrax:
            totaltrax.append(show)

for show in totaltrax:
    if 'showdate' in show:
        showdate = show['showdate']
#        pprint (showdate)
        # eg "Sat 26 Oct 2013" => 2013-10-26
        m = re.match("^(.+) (.+) (.*) (.*)$", showdate)
        if m is not None:
            day = m.group(2)
            if len(day) == 1:
                day = "0" + day
            month = m.group(3)
            year = m.group(4)
#            pprint (month)
            for key in date_dict:
                if date_dict[key] == month:
                    pprint("newdate: " + key )
                    month = key
            newdate = year + "-" + month + "-" + day
            show['showdate'] = newdate
#            pprint("NEWDATE: " + newdate)

with open("datefixed_file.json", "w") as outfile:
     json.dump(totaltrax, outfile, indent=2, sort_keys=True)