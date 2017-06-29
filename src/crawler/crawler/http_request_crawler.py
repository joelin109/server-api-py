from src.crawler.crawler.http_request import HttpRequest, HttpURlParse


class ArticleHttpRequestCrawler(HttpRequest):
    soup_match_count = 0

    def __init__(self, parser: HttpURlParse):
        super().__init__(parser)

    def start(self):
        _soup = self.request_result()
        self.parse_soup_result(_soup, self.html_parse_div_tag)

        self._start_parse()

    def _start_parse(self):
        if self.soup_body is not None:
            _soup_body_count = len(self.soup_body)
            if _soup_body_count >= 1:
                for _soup_body in self.soup_body:
                    _soup_body_html_text = self._parse_soup_to_html_text(_soup_body)
                    self.soup_html_text += _soup_body_html_text + '<p></p>'

    def _parse_soup_to_html_text(self, soup):
        _soup_body = self._clean_soup_useless_tags(soup)
        print(_soup_body.prettify())

        _soup_body_text = str(_soup_body).replace('<a href=', '<a target=\"_blank\" href=')
        return _soup_body_text

    def get_crawl_result(self):
        return self.soup_html_text, self.soup_match_count, self.url_status,


class WordHttpRequestCrawler(HttpRequest):
    soup_match_count = 0

    def __init__(self, parser: HttpURlParse):
        super().__init__(parser)

    def start(self):
        _soup = self.request_result()
        self.parse_soup_result(_soup, self.html_parse_div_tag)

        self._start_parse()

    def _start_parse(self):
        if self.soup_body is not None:
            _soup_body_count = len(self.soup_body)
            if _soup_body_count >= 1:
                for _soup_body in self.soup_body:
                    _soup_body_html_text = self._parse_soup_to_html_text(_soup_body)
                    self.soup_html_text += _soup_body_html_text + '<p></p>'

    def _parse_soup_to_html_text(self, soup):
        _soup_body = self._clean_soup_useless_tags(soup)
        #print(_soup_body.prettify())

        print(_soup_body.find_all("span", class_="Phonitic-Sep"))
        print(_soup_body.find_all("span", class_="Phonitic"))

        _soup_body_text = str(_soup_body)
        return _soup_body_text

    def get_crawl_result(self):
        return self.soup_html_text, self.soup_match_count, self.url_status,
