from src.crawler.crawler.word_http_crawler import WordHttpCrawler, HttpUrlRule


def request_crawl_words(word: str=None):
    if word is None:
        word = 'sauer'
    return request_crawl_word(word)


def request_crawl_word(word):
    _url = 'https://www.godic.net/dicts/de/%s' % word
    _rule = HttpUrlRule(_url)
    _rule.display()

    if _rule.html_parse_body_tag == '':
        return 'Please set parse rule first'
    else:
        _crawler = WordHttpCrawler(_rule)
        _crawler.start()

        _crawl_body_text, _count, _status = _crawler.get_crawl_result()
        return _crawl_body_text