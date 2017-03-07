- ir_scrape to rip all modern iPlayer sites ...

- pre_ir_scrape is for the pre-iPlayer online archive eg Worldwide 2002-09

- use merger script to merge the multiple files

- use datefixer to standardise the dates to YYYY-MM-DD

- Now you have datefixed json! a complete index

- Pretty print:
json_pp -f json < datefixed.json  > pp_fullindex.json

- do pre_ir_scrape
-- do artisttruncer.py
-- do blurbfixer.py
-- do blurbconverter.py
-- do labelfixer.py

- now I think it's almost clean! Just a few dirty blurbs ...
