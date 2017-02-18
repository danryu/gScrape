# irScrape

A quick utility to scrape the BBC iPlayer website for tracklisting information.
Each show has the following information extracted:
- Date
- Title
- Synopsis
- Tracklist featuring each:
  - artist
  - tracktitle
  - label (where supplied)

Install requirements by doing ``` pip install -r requirements.txt```

Usage: 

``` scrapy crawl ir_scrape -o output_file.json ```

See the comments in the code for how to set the sites to scrape.
(set "start_urls" value, basically)
