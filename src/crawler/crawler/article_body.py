from src.crawler.crawler.http_request_crawler import ArticleHttpRequestCrawler, HttpUrlRule


def request_crawl_article_bodys():
    _url = 'http://ew.com/news/2017/04/30/hasan-minhaj-trump-spicer-white-house-correspondents-dinner-best-jokes/'
    _url2 = 'https://arstechnica.com/the-multiverse/2017/04/colossal-review-everyone-has-a-monster-most-arent-this-fun/'
    _crawl_body_text = crawl_http_url(_url)
    # print(_crawl_body_text)
    return ''


def crawl_http_url(crawl_url=None):
    _url = '' if crawl_url is None else crawl_url
    _rule = HttpUrlRule(_url)
    _rule.display()

    if _rule.html_parse_body_tag == '':
        return 'Please set parse rule first'
    else:
        _crawler = ArticleHttpRequestCrawler(_rule)
        _crawler.start()
        _crawl_body_text, _count, _status = _crawler.get_crawl_result()
        return _crawl_body_text
