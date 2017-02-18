# -*- coding: utf-8 -*-
import scrapy
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
    # eg start_urls = ['http://www.bbc.co.uk/programmes/b01fm4ss/broadcasts/2016/01']
    # start_urls = ['http://www.bbc.co.uk/programmes/b01fm4ss/broadcasts/2016/01']
    # for May 2002 - Oct 2009 - DIFFERENT CRAWLER
    start_urls = ['http://www.bbc.co.uk/radio1/gillespeterson/tracklistings200']
    # start_urls = ['http://www.bbc.co.uk/radio1/gillespeterson/tracklistings200[2-9].shtml']
    
    # different crawler...
    # for Nov 2009 - Mar 2012
    #start_urls = ['http://www.bbc.co.uk/programmes/b006wq8d/broadcasts']
    # for April 2012 - current
    #start_urls = ['http://www.bbc.co.uk/programmes/b01fm4ss/broadcasts/']

    def start_requests(self):
        for year in range(2,10):
            url = self.start_urls[0] + str(year) + ".shtml"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        for show in response.css("div.br-box-page.programmes-page ol li"):
            show_url = show.css("div div div.broadcast__programme.grid.three-quarters.bpb2-five-sixths.bpw-five-sixths div div.programme__body h4.programme__titles a::attr(href)").extract_first()
            print ("SHOW_URL:" + show_url)
            if show_url is not None:
                show_url = response.urljoin(show_url)
                yield scrapy.Request(show_url, callback=self.parse_show)

    def parse_show(self, response):
        p_tracklist = Tracklist()
    
        pr_showdate = response.css("#programmes-main-content div.b-g-p.no-margin-vertical div div.grid.bpw2-one-third.bpe-one-third.map__column.map__column--2.map__column--last div div div.programme__body.programme__body--flush div.broadcast-event__time.beta span.broadcast-event__date.text-base.timezone--date::text").extract_first()
        p_tracklist['showdate'] = pr_showdate
        p_tracklist['showname'] = response.css("#programmes-main-content div.b-g-p.no-margin-vertical div div.grid.bpw2-two-thirds.bpe-two-thirds.map__column.map__column--first div div.island div:nth-child(1) h1::text").extract()
        
        desc_list = []
        for paragraph in response.css("#programmes-main-content > div.b-g-p.no-margin-vertical > div > div.grid.bpw2-two-thirds.bpe-two-thirds.map__column.map__column--first > div > div.island > div.grid-wrapper > div.grid.bpw-two-thirds.bpe-three-quarters > div > div > div.map__intro__synopsis.centi"):
            desc_list.append(paragraph.css("p::text").extract())
            #FIXME random extra bit in pages like 23.1.2016 - but hardly anything really .....
#            extra_bit = paragraph.css("p span::text").extract()
#            if extra_bit is not None:
#                desc_list.append(extra_bit)
        p_tracklist['showdesc'] = desc_list
        
    # FIXME - no need to loop here
        for playlist in response.css("#segments"):
            playlist_url = playlist.css("div.lazy-module.lazy-module--loading--loader::attr(data-lazyload-inc)").extract_first()
            if playlist_url is not None:
                playlist_url = response.urljoin(playlist_url)
                play_req = scrapy.Request(playlist_url, callback=self.parse_playlist)
                play_req.meta['tracklist'] = p_tracklist
                yield play_req
        
        file = open('%s_tracklist.json' % pr_showdate, 'w+b')
        jsonExporter = JsonItemExporter(file)
        jsonExporter.export_item(p_tracklist)


    def parse_playlist(self, response):
        tracklist = response.meta['tracklist']
        t_list = []
        index = 1
        
        # FIXME - need to switch on "sub-class" of li element
        for track in response.css("#segments div.component__body.br-box-page div ul li"):
            # EXAMPLES 
            # kode9 ... http://www.bbc.co.uk/programmes/b00q8xs9
            # ed motta .. http://www.bbc.co.uk/programmes/b06whk5b

            item_class = track.css("li::attr(class)").extract()

            # The main itemtype, Tracklist entry
            if item_class[0].startswith("segments-list__item segments-list__item--music"):
                track_entry = {
                    'index': index,
                    #FIXME fix "space ape" tune -  also as in http://www.bbc.co.uk/programmes/b00q8xs9 kode9: (space ape tune) #segments > div.component__body.br-box-page > div > ul > li:nth-child(9) > ul > li:nth-child(3) > div > div.segment__content.segment--withbuttons > div.segment__track > p > span
                    'artist': track.css("h3 span span.artist::text").extract_first(),
                    #FIXME check for "feat: " also in trackname
                    'trackname': track.css("p span::text").extract_first(),
                    'label': track.css("ul li span::text").extract_first()
                }
                # Fix for h4
                if track_entry['artist'] is None:
                    track_entry['artist'] = track.css("h4 span span.artist::text").extract_first()
                #print ("TRACK: %s" % track_entry)
                t_list.append(track_entry)
                index = index+1
            
            # For when the list entry is a Guest mix, or Words and Music section. Just grab title. Getting the full length of section too complex for now
            if item_class[0].startswith("segments-list__item segments-list__item--group"):
                #print ("SUBMIX NAME: %s" % track.css("h3::text").extract_first())
                submix_entry = {
                    'index': index,
                    'title': track.css("h3::text").extract_first()
                }
                t_list.append(submix_entry)
                index = index+1
            
            # For another itemtype, when it's a separate words-only segment ... quite rare but it happens....
            if item_class[0].startswith("segments-list__item.segments-list__item--speech"):
                speechbit_entry = {
                    'index': index,
                    'blurb': track.css("h4::text").extract(),
                }
                t_list.append(speechbit_entry)
                #print ("SPEECHBIT: %s" % speechbit_entry)
                index = index+1
                
            # end track iteration
        tracklist['showtrax'] = t_list
        #print ("TLIST...%s" % t_list)
        return tracklist
        
