from bs4 import BeautifulSoup
import re
import requests
from src.service.crawler.article_body_parse_rule import crawl_http_url_parse_rule, crawl_http_article_body_html


def request_crawl_article_bodys():
    _url = 'http://ew.com/news/2017/04/30/hasan-minhaj-trump-spicer-white-house-correspondents-dinner-best-jokes/'
    _url2 = 'https://arstechnica.com/the-multiverse/2017/04/colossal-review-everyone-has-a-monster-most-arent-this-fun/'
    _crawl_body_text = crawl_article_body(_url)
    # print(_crawl_body_text)
    return ''


def crawl_article_body(crawl_url=None):
    _url = '' if crawl_url is None else crawl_url
    # _url = 'https://www.washingtonpost.com/posteverything/wp/2017/02/16/my-grandfather-helped-create-captain-america-for-times-like-these/?utm_term=.c60914db592f'
    _parse_rule, _del_div_tags = crawl_http_url_parse_rule(_url)
    if _parse_rule == '':
        return 'Please set parse rule first'
    else:
        print(_url + '  |  ' + _parse_rule)
        _crawl_body_text, _status = _crawler_article_body(_url, _parse_rule, _del_div_tags)
        return _crawl_body_text


def _crawler_article_body(url, parse_rule, del_div_tags):
    _body_parse_rule = parse_rule

    _user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    _response = requests.get(url, headers={'User-Agent': _user_agent})
    _response.encoding = 'utf-8'
    _soup = BeautifulSoup(_response.text, "lxml")

    # _soup_bodys = _soup.find_all("div", _body_parse_rule)
    # _soup_bodys = _soup.find_all(lambda tag: tag.get('class') == [_body_parse_rule])
    # _soup_bodys = _soup.find_all(attrs={'class': re.compile(r'^' + _body_parse_rule + '$')})
    _soup_bodys = _soup.find_all(attrs={'class': re.compile(r'' + _body_parse_rule)})

    _soup_body_count = len(_soup_bodys)
    if _soup_body_count == 0:
        return '', _soup_body_count
    elif _soup_body_count == 1:
        _soup_body_html_text = _crawler_article_body_html_text(_soup_bodys[0], del_div_tags)
        return _soup_body_html_text, _soup_body_count
    else:
        _soup_body_html_texts = ''
        for _soup_body in _soup_bodys:
            _soup_body_html_text = _crawler_article_body_html_text(_soup_body, del_div_tags)
            _soup_body_html_texts += _soup_body_html_text + '<p></p><p></p>'

        return _soup_body_html_texts, _soup_body_count


def _crawler_article_body_html_text(soup, del_div_tags):
    _soup_body = crawl_http_article_body_html(soup, del_div_tags)
    _soup_body_text = str(_soup_body).replace('<a href=', '<a target=\"_blank\" href=')
    return _soup_body_text


def _update_article_body(article_id, body_text):
    print(article_id)

    return ''
