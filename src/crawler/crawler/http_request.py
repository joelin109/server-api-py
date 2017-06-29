from bs4 import BeautifulSoup, Comment
import re
import requests
from src.crawler.crawler.http_url_parse_setting import HttpURlParse
from src.crawler.crawler.html_parse_util import clean_reset_body_html

_user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'


class HttpRequest:
    url = ''
    html_parse_div_tag = ''
    will_del_h5_tags = ['figcaption', 'script', 'aside', 'video']
    will_del_div_tags = ['share-icons', 'inner-wrapper', 'article-tags', 'view-content', 'newsletter-signup']

    url_status = 200
    soup_body = None
    soup_html_text = ''

    def __init__(self, parser: HttpURlParse):
        self.url = parser.url
        self.html_parse_div_tag = parser.html_parse_body_tag
        self.will_del_h5_tags = parser.will_del_h5_tags
        self.will_del_div_tags = parser.will_del_div_tags

    def request_result(self):
        _response = requests.get(self.url, headers={'User-Agent': _user_agent})
        _response.encoding = 'utf-8'
        return BeautifulSoup(_response.text, "lxml")

    def parse_soup_result(self, soup, div_tag: str=None, tag_type: str = 'class'):

        try:
            if div_tag is None:
                div_tag = self.html_parse_div_tag

            # _soup_bodys = _soup.find_all("div", _body_parse_rule)
            # _soup_bodys = _soup.find_all(lambda tag: tag.get('class') == [_body_parse_rule])
            # _soup_bodys = _soup.find_all(attrs={'class': re.compile(r'^' + _body_parse_rule + '$')})
            if tag_type == 'class':
                self.soup_body = soup.find_all(attrs={'class': re.compile(r'' + div_tag)})
            else:
                self.soup_body = soup.find_all(attrs={'id': re.compile(r'' + div_tag)})

        except Exception as ex:
            self.soup_html_text = str(ex)[0:500]

    def _clean_soup_useless_tags(self, soup):
        self.__clean_common_useless_h5(soup, self.will_del_h5_tags)
        return self.__clean_useless_div(soup, self.will_del_div_tags)

    def __clean_useless_div(self, soup, div_tags=None):
        if div_tags is None:
            div_tags = self.will_del_div_tags

        return clean_reset_body_html(soup, div_tags)

    def __clean_common_useless_h5(self, soup, h5_tags):
        if h5_tags is None:
            h5_tags = self.will_del_h5_tags

        for element in soup(text=lambda text: isinstance(text, Comment)):
            element.extract()

        for _del_h5_tag in h5_tags:
            [s.extract() for s in soup(_del_h5_tag)]

        _del_div_re_classes = ['hidden', '-wrapper']
        for _del_div_re_class in _del_div_re_classes:
            [s.extract() for s in soup.find_all(attrs={'class': re.compile(r'' + _del_div_re_class)})]

    def display(self):
        print(self.url + '  |  ' + self.html_parse_div_tag, self.will_del_div_tags)

    def _find_class(self, soup, class_tag: str):
        return soup.find_all(attrs={'class': re.compile(r'' + class_tag)})
