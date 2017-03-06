# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.exporters import JsonItemExporter

class Tracklist(scrapy.Item):
    showdate = scrapy.Field()
    showname = scrapy.Field()
    showdesc = scrapy.Field()
    showtrax = scrapy.Field()
    showurl = scrapy.Field()

class pre_IRScrapeSpider(scrapy.Spider):
    name = "pre_ir_scrape"
    allowed_domains = ["www.bbc.co.uk"]
    # for May 2002 - Oct 2009
    #start_urls = ['http://www.bbc.co.uk/radio1/gillespeterson/tracklistings2008.shtml']
    start_urls = ['http://www.bbc.co.uk/radio1/gillespeterson/tracklistings200']
    # start_urls = ['http://www.bbc.co.uk/radio1/gillespeterson/tracklistings200[2-9].shtml']

    def start_requests(self):
        for year in range(2,10):
            url = self.start_urls[0] + str(year) + ".shtml"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for show in response.css("#tracklisting_wrapper div div"):
            p_tracklist = Tracklist()
            # get Show URL
            showurl = show.css("p.date a::attr(href)").extract_first()
            if showurl is not None:
                p_tracklist['showurl'] = showurl
                # get Show Date
                m = re.match('.*(20..)(..)(..)$', p_tracklist['showurl'])
                if m is not None:
                    p_tracklist['showdate'] =  "{0}-{1}-{2}".format(m.group(1), m.group(2), m.group(3))
                # get Show Name
                p_tracklist['showname'] =  show.css("p.info::text").extract_first()
                # go parse Show
                show_url = p_tracklist['showurl']
                if show_url is not None:
                    show_url = response.urljoin(show_url)
                    play_req = scrapy.Request(show_url, callback=self.parse_show)
                    play_req.meta['tracklist'] = p_tracklist
                    yield play_req
#main-rm > div:nth-child(2)
#main-rm > div:nth-child(2)
#main-rm > div:nth-child(3)
                    
    def parse_show(self, response): 
        tracklist = response.meta['tracklist']
        tracklist['showurl'] = response.url
        t_list = []
        index = 1
        for track in response.css("#main-rm div:nth-child(2)"):
        #for track in response.css("#main-rm div font"):
        #for track in response.css("#main-rm div font::text"):
            #print ("TRAAAAACK: %s" % track)
            #print ("TRACCK SUBS: %s " % track.extract())
            for line in track.extract().split("\r\n"):
                for brline in line.split("<br>"):
                    brline = brline.strip()
                    # remove all kinds of tags
                    brline = re.sub('<.*tracklisting_archive_container.*>', '', brline)
                    brline = re.sub('<.*hand\ aligned\ image.*', '', brline)
                    brline = re.sub('<.*font.*?>', '', brline) 
                    brline = re.sub('</?strong>', '', brline) 
                    brline = re.sub('<.?b.?>', '', brline)
                    brline = re.sub('</a>', '', brline)
                    brline = re.sub('<.*em.*?>', '', brline)
                    #brline = re.sub('<.*u.*?>', '', brline)
                    brline = re.sub('</div>', '', brline) 
                    brline = re.sub('<.*span.*>', '', brline)
                    brline = re.sub('<.*p>', '', brline) 
                    # remove time line
                    brline = re.sub('0?[23][\.\:]00', '', brline)
                    
                    if brline != "":
                        # get rid of 
                        # assume it's a track if we have: asdasdasdasd-'asdadasdasd'....
                        m = re.match("(.*?)([-–­] | [-–­])(.*)$", brline)
                        if m is not None: # we have a track
                            artist = m.group(1)
                            tracktitle = m.group(3)
                            track_entry = {
                                'index': index,
                                'artist': artist,
                                'trackname': tracktitle
                            }
                            # match label if we can, last pair of brackets (could be a first re-edit bracket set, say)
                            l = re.match("^(.*)(\(.*\)){1}", tracktitle)
                            if l is not None:
                                track_entry['label'] = l.group(2)
                                track_entry['trackname'] = l.group(1) 
                        # catch malformed tracklines
                        else:
                            n = re.match("(.*?)([\'\"].*[\'\"])(\(.*\))$", brline)
                            if n is not None: # we have a track
                                artist = n.group(1)
                                tracktitle = n.group(2)
                                label = n.group(3)
                                track_entry = {
                                    'index': index,
                                    'artist': artist,
                                    'trackname': tracktitle,
                                    'label': label
                                }
                            else: # it's a chapter title
                                track_entry = {
                                    'index': index,
                                    'blurb': brline
                                }
                            # FIX for this brokenness:
                                # Valley' (Intro) (Sonar Kollektiv)
                                # Switch &amp; Rusko 'Untitled' (White)"
                                # Baby Charles ‘Trading Water’ (RK Record Kicks)
#                            b = re.match("(.*?)([‘'].*['’]).*(\(.*\))", brline)
#                            if b is not None:
#                                track_entry = {
#                                    'index': index,
#                                    'artist': group(1),
#                                    'trackname': group(2),
#                                    'label': group(3)
#                                }
                        
                        # final clean...
                        # remove ‘’' from trackname
                        if 'trackname' in track_entry:
                            r = re.match(".*[‘’'].*", track_entry['trackname'])
                            if r is not None:
                                track_entry['trackname'] = re.sub('[‘’\']', '', track_entry['trackname'])
                            track_entry['trackname'] = track_entry['trackname'].strip()
                        
                        # remove () from label
                        if 'label' in track_entry:
                            l = re.match(".*[()].*", track_entry['label'])
                            if l is not None:
                                track_entry['label'] = re.sub('[\(\)]', '', track_entry['label'])
                            track_entry['label'] = track_entry['label'].strip()   
                            
                        # remove \ from blurb
                        if 'blurb' in track_entry:
                            l = re.match(".*[\\\].*", track_entry['blurb'])
                            if l is not None:
                                track_entry['blurb'] = re.sub('[\\\]', '', track_entry['blurb'])
                            track_entry['blurb'] = track_entry['blurb'].strip()  
                        
                        # HACKFIX for some reason some blurbs end up empty here
                        if 'blurb' in track_entry:
                            if track_entry['blurb'] != "":
                                t_list.append(track_entry)
                        # all normal tracks
                        else:
                            t_list.append(track_entry)
                        index = index + 1
        tracklist['showtrax'] = t_list
        return tracklist
        

