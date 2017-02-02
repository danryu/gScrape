# -*- coding: utf-8 -*-
import scrapy

class GillesripSpider(scrapy.Spider):
  name = "gillesRip"
  allowed_domains = ["www.bbc.co.uk"]
  start_urls = ['http://www.bbc.co.uk/programmes/b01fm4ss/broadcasts/2017/01/']

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
      print ("SHHHHHHHHHHHHHHOW:" + show_url)
      if show_url is not None:
        show_url = response.urljoin(show_url)
        yield scrapy.Request(show_url, callback=self.parse_show)

  def parse_show(self, response):
#    def extract_with_css(query):
#      return response.css(query).extract_first().strip()

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


  def parse_playlist(self, response):
    for track in response.css("#segments div.component__body.br-box-page div ul li"):
      print (track.extract())
