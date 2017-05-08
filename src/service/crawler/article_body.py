from src.service.crawler.http_html_crawler import HttpHtmlCrawler
from src.service.crawler.http_url_parse_setting import HttpURlParse


def request_crawl_article_bodys():
    _url = 'http://ew.com/news/2017/04/30/hasan-minhaj-trump-spicer-white-house-correspondents-dinner-best-jokes/'
    _url2 = 'https://arstechnica.com/the-multiverse/2017/04/colossal-review-everyone-has-a-monster-most-arent-this-fun/'
    _crawl_body_text = crawl_http_url(_url)
    # print(_crawl_body_text)
    return ''


def crawl_http_url(crawl_url=None):
    _url = '' if crawl_url is None else crawl_url
    # _url = 'https://www.washingtonpost.com/posteverything/wp/2017/02/16/my-grandfather-helped-create-captain-america-for-times-like-these/?utm_term=.c60914db592f'

    _parse = HttpURlParse(_url)
    _parse.display()
    if _parse.html_parse_body_tag == '':
        return 'Please set parse rule first'
    else:
        _crawler = HttpHtmlCrawler(_parse)
        _crawler.start()
        _crawl_body_text, _count, _status = _crawler.get_crawl_result()
        return _crawl_body_text
