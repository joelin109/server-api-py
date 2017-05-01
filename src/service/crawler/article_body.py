from bs4 import BeautifulSoup
import requests


def request_crawl_article_bodys():
    _url = 'http://ew.com/news/2017/04/30/hasan-minhaj-trump-spicer-white-house-correspondents-dinner-best-jokes/'
    _url2 = 'https://arstechnica.com/the-multiverse/2017/04/colossal-review-everyone-has-a-monster-most-arent-this-fun/'
    _parse_url = _url2
    _parse_rule = _crawler_body_parse_rule(_parse_url)

    print(_parse_url + '  |  ' + _parse_rule)
    _crawl_body_text = _crawler_body(_parse_url, _parse_rule)
    print(_crawl_body_text)
    return ''


def _crawler_body(url, parse_rule):
    _body_parse_rule = parse_rule
    _response = requests.get(url)
    _soup = BeautifulSoup(_response.text, 'html.parser')

    _soup_body = _soup.find_all("div", _body_parse_rule)
    _body_text = _soup_body
    return _body_text


def _crawler_body_parse_rule(url):
    if url.find('ew.com') > 0:
        return 'article-body__inner'

    if url.find('arstechnica.com') > 0:
        return 'article-content post-page'


def _update_article_body(article_id, body_text):
    print(article_id)

    return ''
