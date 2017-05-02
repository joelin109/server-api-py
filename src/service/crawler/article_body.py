from bs4 import BeautifulSoup, Comment
import requests


def request_crawl_article_bodys():
    _url = 'http://ew.com/news/2017/04/30/hasan-minhaj-trump-spicer-white-house-correspondents-dinner-best-jokes/'
    _url2 = 'https://arstechnica.com/the-multiverse/2017/04/colossal-review-everyone-has-a-monster-most-arent-this-fun/'
    _crawl_body_text = crawl_article_body(_url)
    print(_crawl_body_text)
    return ''


def crawl_article_body(crawl_url=None):
    _url = '' if crawl_url is None else crawl_url
    # _url = 'https://arstechnica.com/gaming/2017/05/half-life-portal-scribe-leaves-valve/'
    _parse_rule = _crawler_body_parse_rule(_url)
    if _parse_rule == '':
        return 'Please set parse rule first'
    else:
        print(_url + '  |  ' + _parse_rule)
        _crawl_body_text = _crawler_body(_url, _parse_rule)
        return _crawl_body_text


def _crawler_body(url, parse_rule):
    _body_parse_rule = parse_rule
    _response = requests.get(url)
    _soup = BeautifulSoup(_response.text, 'html.parser')

    _soup_body = _soup.find_all("div", _body_parse_rule)[0]
    _soup_body_html = _crawler_body_html(_soup_body)

    # print(type(_soup_body))
    _body_text = str(_soup_body)
    return _body_text


def _crawler_body_html(soup):
    _soup_body = soup
    [s.extract() for s in _soup_body('figcaption')]
    [s.extract() for s in _soup_body('script')]
    [s.extract() for s in _soup_body('figure')]
    [s.extract() for s in _soup_body('aside')]
    for element in _soup_body(text=lambda text: isinstance(text, Comment)):
        element.extract()

    print(_soup_body.prettify())
    return _soup_body


def _crawler_body_parse_rule(url):
    # ars - technica
    if url.find('arstechnica.com') > 0:
        return 'article-content post-page'

    # buzzfeed ?
    if url.find('www.buzzfeed.com') > 0:
        return ''

    # cnn ?
    if url.find('www.cnn.com') > 0:
        return ''

    # der-tagesspiegel ?
    if url.find('www.tagesspiegel.de') > 0:
        return ''

    # google-news ? from everywhere
    if url.find('www.nytimes.com') > 0:
        return 'story-body-supplemental'

    # bbc-news
    if url.find('www.bbc.co.uk') > 0:
        return 'story-body__inner'
    if url.find('www.bbc.com') > 0:
        return 'story-body__inner'

    # entertainment-weekly
    if url.find('ew.com') > 0:
        return 'article-body__inner'

    # the-new-york-times ?
    if url.find('www.nytimes.com') > 0:
        return ''

    # wired-de ?
    if url.find('www.wired.de') > 0:
        return ''

    return ''


def _update_article_body(article_id, body_text):
    print(article_id)

    return ''
