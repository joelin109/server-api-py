from src.crawler.crawler.http_request_crawler import WordHttpRequestCrawler
from src.crawler.crawler.http_url_parse_setting import HttpURlParse


def request_crawl_words(word: str=None):
    if word is None:
        word = 'sauer'
    return request_crawl_word(word)


def request_crawl_word(word):
    _url = 'https://www.godic.net/dicts/de/%s' % word
    _parse = HttpURlParse(_url)
    _parse.display()

    if _parse.html_parse_body_tag == '':
        return 'Please set parse rule first'
    else:
        _crawler = WordHttpRequestCrawler(_parse)
        _crawler.start()

        _crawl_body_text, _count, _status = _crawler.get_crawl_result()
        return _crawl_body_text