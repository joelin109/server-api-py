from scrapy import cmdline
from src.crawler.scrapy.spiders.db_book import crawl_name

_execute = 'scrapy crawl ' + crawl_name
cmdline.execute(_execute.split())
