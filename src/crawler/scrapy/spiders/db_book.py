# -*- coding: utf-8 -*-
import scrapy
import re
from src.crawler.scrapy.items import CrawlerItem
crawl_name = 'db_book2'


class DbbookSpider(scrapy.Spider):
    name = crawl_name
    # allowed_domains = ["https://www.douban.com/doulist/1264675/"]
    start_urls = (
        'https://www.douban.com/doulist/1264675/',
    )
    URL = 'https://www.douban.com/doulist/1264675/?start=PAGE&sort=seq&sub_type='

    def parse(self, response):
        # print response.body
        item = CrawlerItem()
        selector = scrapy.Selector(response)
        _books = selector.xpath('//div[@class="bd doulist-subject"]')

        for _book in _books:
            _title = _book.xpath('div[@class="title"]/a/text()').extract()[0].strip()
            _rating_num = _book.xpath('div[@class="rating"]/span[@class="rating_nums"]/text()').extract()
            _rate = '?' if len(_rating_num) == 0 else _rating_num[0].strip()
            _author = re.search('<div class="abstract">(.*?)<br', _book.extract(), re.S).group(1).strip()
            print('Spider:' + _title + ' | ' + _rate + ' | ' + _author)
            item['title'] = _title
            item['rate'] = _rate
            item['author'] = _author
            # yield item

        _next_page = selector.xpath('//span[@class="next"]/link/@href').extract()
        if _next_page:
            _next_page_src = _next_page[0]
            print(_next_page_src)
            # yield scrapy.http.Request(_next_page_src, callback=self.parse)
