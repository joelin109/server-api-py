from bs4 import BeautifulSoup, Comment
import re
import requests
from src.crawler.crawler.http_url_parse_setting import HttpURlParse
from src.crawler.crawler.html_parse_util import clean_reset_body_html


class HttpHtmlCrawler:
    url = ''
    url_status = 200
    html_parse_body_tag = ''
    will_del_h5_tags = ['figcaption', 'script', 'aside', 'video']
    will_del_div_tags = ['share-icons', 'inner-wrapper', 'article-tags', 'view-content', 'newsletter-signup']
    soup_body = None
    soup_match_count = 0
    soup_html_text = ''

    def __init__(self, parser: HttpURlParse):
        self.url = parser.url
        self.html_parse_body_tag = parser.html_parse_body_tag
        self.will_del_h5_tags = parser.will_del_h5_tags
        self.will_del_div_tags = parser.will_del_div_tags

    def start(self):
        self._start_crawl()
        self._start_parse()

    def _start_crawl(self):
        _user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        try:
            _response = requests.get(self.url, headers={'User-Agent': _user_agent})
            _response.encoding = 'utf-8'
            _soup = BeautifulSoup(_response.text, "lxml")

            # _soup_bodys = _soup.find_all("div", _body_parse_rule)
            # _soup_bodys = _soup.find_all(lambda tag: tag.get('class') == [_body_parse_rule])
            # _soup_bodys = _soup.find_all(attrs={'class': re.compile(r'^' + _body_parse_rule + '$')})
            self.soup_body = _soup.find_all(attrs={'class': re.compile(r'' + self.html_parse_body_tag)})
        except Exception as ex:
            self.soup_html_text = str(ex)[0:500]

    def _start_parse(self):
        if self.soup_body is not None:
            _soup_body_count = len(self.soup_body)
            if _soup_body_count >= 1:
                for _soup_body in self.soup_body:
                    _soup_body_html_text = self._parse_soup_body_html_text(_soup_body)
                    self.soup_html_text += _soup_body_html_text + '<p></p>'

    def _parse_soup_body_html_text(self, soup):
        self._clean_common_useless_html(soup)

        _soup_body = clean_reset_body_html(soup, self.will_del_div_tags)
        _soup_body_text = str(_soup_body).replace('<a href=', '<a target=\"_blank\" href=')
        return _soup_body_text

    def _clean_common_useless_html(self, soup):
        for element in soup(text=lambda text: isinstance(text, Comment)):
            element.extract()

        for _del_h5_tag in self.will_del_h5_tags:
            [s.extract() for s in soup(_del_h5_tag)]

        _del_div_re_classes = ['hidden', '-wrapper']
        for _del_div_re_class in _del_div_re_classes:
            [s.extract() for s in soup.find_all(attrs={'class': re.compile(r'' + _del_div_re_class)})]

    def display(self):
        print(self.url + '  |  ' + self.html_parse_body_tag)
        print(self.will_del_div_tags)

    def get_crawl_result(self):
        return self.soup_html_text, self.soup_match_count, self.url_status,
