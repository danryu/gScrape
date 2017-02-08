# -*- coding: utf-8 -*-
import scrapy
from scrapy.exporters import JsonItemExporter

class Tracklist(scrapy.Item):
    showdate = scrapy.Field()
    showname = scrapy.Field()
    showdesc = scrapy.Field()
    showtrax = scrapy.Field()
    

class GillesripSpider(scrapy.Spider):
    name = "gillesRip"
    allowed_domains = ["www.bbc.co.uk"]
    start_urls = ['http://www.bbc.co.uk/programmes/b01fm4ss/broadcasts/2016/01/']

#    for url in start_urls:
 #       yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for show in response.css("div.br-box-page.programmes-page ol li"):
            yield {
            'time': show.css("div div div.broadcast__info.grid.one-quarter.bpb2-one-sixth.bpw-one-sixth div h3 span.timezone--time::text").extract(),
            'date': show.css("div div div.broadcast__info.grid.one-quarter.bpb2-one-sixth.bpw-one-sixth div h3 span.micro.timezone--date::text").extract(),
            'title': show.css("div div div.broadcast__programme.grid.three-quarters.bpb2-five-sixths.bpw-five-sixths div div.programme__body h4.programme__titles a span.programme__title span::text").extract(),
            'url': show.css("div div div.broadcast__programme.grid.three-quarters.bpb2-five-sixths.bpw-five-sixths div div.programme__body h4.programme__titles a::attr(resource)").extract(),
            'suffixurl': show.css("div div div.broadcast__programme.grid.three-quarters.bpb2-five-sixths.bpw-five-sixths div div.programme__body h4.programme__titles a::attr(href)").extract(),
            'synopsis': show.css("div div div.broadcast__programme.grid.three-quarters.bpb2-five-sixths.bpw-five-sixths div div.programme__body p.programme__synopsis.text--subtle.centi span::text").extract()
            }

            show_url = show.css("div div div.broadcast__programme.grid.three-quarters.bpb2-five-sixths.bpw-five-sixths div div.programme__body h4.programme__titles a::attr(href)").extract_first()
            print ("SHOW_URL:" + show_url)
            if show_url is not None:
                show_url = response.urljoin(show_url)
                yield scrapy.Request(show_url, callback=self.parse_show)

    def parse_show(self, response):
    #    def extract_with_css(query):
    #      return response.css(query).extract_first().strip()
        pr_showdate = response.css("#programmes-main-content div.b-g-p.no-margin-vertical div div.grid.bpw2-one-third.bpe-one-third.map__column.map__column--2.map__column--last div div div.programme__body.programme__body--flush div.broadcast-event__time.beta span.broadcast-event__date.text-base.timezone--date::text").extract_first()
        print ('SHOOOOOOOOOOWDATE: %s' % pr_showdate)
        
    # FIXME - no need to loop here, can just extract_with_css as above...
        for playlist in response.css("#segments"):
            yield {
                'wholeblock': playlist.css("div.lazy-module.lazy-module--loading--loader").extract(),
                'playlist_url': playlist.css("div.lazy-module.lazy-module--loading--loader::attr(data-lazyload-inc)").extract()
            }

            playlist_url = playlist.css("div.lazy-module.lazy-module--loading--loader::attr(data-lazyload-inc)").extract_first()
            if playlist_url is not None:
                playlist_url = response.urljoin(playlist_url)
                yield scrapy.Request(playlist_url, callback=self.parse_playlist)
        
        # save:
        # Show date #programmes-main-content > div.b-g-p.no-margin-vertical > div > div.grid.bpw2-one-third.bpe-one-third.map__column.map__column--2.map__column--last > div > div:nth-child(1) > div > div > div.programme__body.programme__body--flush > div.broadcast-event__time.beta > span.broadcast-event__date.text-base.timezone--date
        # Show name
        # Show description
        # Show image - maybe
        # Show tracklist
            # 01 artist trackname label
            # 02 .................
        file = open('%s_tracklist.json' % pr_showdate, 'w+b')
        jsonExporter = JsonItemExporter(file)
        tracklist = Tracklist(showdate=pr_showdate)
        jsonExporter.export_item(tracklist)


    def parse_playlist(self, response):
        for track in response.css("#segments div.component__body.br-box-page div ul li div div.segment__content.segment--withbuttons div.segment__track "):
            yield {
                #FIXME check for h4 as well for segments ...
                # FIXME loop on artist for multiple artist
                'artist': track.css("h3 span span.artist::text").extract_first(),
                #FIXME check for "feat: " also in trackname
                'trackname': track.css("p span::text").extract_first(),
                'label': track.css("ul li span::text").extract_first()
                #FIXME - create index, 01, 02 ....
                #'index': ??
            }
