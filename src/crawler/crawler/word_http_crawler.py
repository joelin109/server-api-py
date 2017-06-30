from src.crawler.crawler.util.http_request import HttpRequest, HttpUrlRule


class WordHttpCrawler(HttpRequest):
    phonitic = ''
    phonitic_sep = ''
    zh = ''
    en = ''

    def __init__(self, rule: HttpUrlRule):
        super().__init__(rule)

        self.soup_match_count = 0

    def start(self):
        _soup = self.request_result()

        self.parse_soup_result(_soup, self.html_parse_div_tag)
        self._start_parse()

        self.parse_soup_result(_soup, 'expDiv')
        _soup_de_zh = self._clean_soup_useless_tags(self.soup_body[0])

        _soup_de_type = _soup_de_zh.find_all("span", class_="cara")

        _soup_zhs = _soup_de_zh.find_all("span", class_="exp")
        for _zh in _soup_zhs:
            self.zh += _zh.getText() + ','

        # print(_soup_zh.prettify())

    def _start_parse(self):
        if self.soup_body is not None:
            _soup_body_count = len(self.soup_body)
            if _soup_body_count >= 1:
                for _soup_body in self.soup_body:
                    self._parse_soup_to_html_text(_soup_body)

    def _parse_soup_to_html_text(self, soup):
        _soup_body = self._clean_soup_useless_tags(soup)
        # print(_soup_body.prettify())

        _soup_phonitic = _soup_body.find_all("span", class_="Phonitic-Sep")
        for _soup in _soup_phonitic:
            self.phonitic_sep = _soup.getText()

        _soup_phonitic = _soup_body.find_all("span", class_="Phonitic")
        for _soup in _soup_phonitic:
            self.phonitic = _soup.getText()

    def get_crawl_result(self):
        _parse_result = {
            "phonitic_sep": self.phonitic_sep,
            "phonitic": self.phonitic,
            "zh": self.zh
        }
        return _parse_result, self.soup_match_count, self.url_status,
