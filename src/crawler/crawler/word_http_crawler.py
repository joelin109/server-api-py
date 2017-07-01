from src.crawler.crawler.util.http_request import HttpRequest, HttpUrlRule
from src.service.model.model_content import ContentDictionary


class WordHttpCrawler(HttpRequest):
    phonitic = ''
    phonitic_sep = ''
    type_desc = ''

    def __init__(self, rule: HttpUrlRule, wort: str=None):
        _wort = '' if wort is None else wort
        self.word: ContentDictionary = ContentDictionary(_wort)
        self.soup_match_count = 0

        super().__init__(rule)

    def start(self):
        _soup = self.request_result()

        self.parse_soup_result(_soup, self.html_parse_div_tag)
        self._start_parse_phonitic()

        self.parse_soup_result(_soup, 'expDiv')

        if len(self.soup_body) > 0:
            _soup_de_zh = self._clean_soup_useless_tags(self.soup_body[0])
            self._start_parse_type(_soup_de_zh)
            self._start_parse_zh(_soup_de_zh)
        else:
            _soup_de_zh = _soup.find_all("div", id="translate")
            print(_soup_de_zh)
            for _soup_de in _soup_de_zh:
                print(_soup_de.getText())

        # print(self.soup_body.getText())

    def _start_parse_phonitic(self):
        if self.soup_body is not None:
            _soup_body_count = len(self.soup_body)
            if _soup_body_count >= 1:
                for _soup_body in self.soup_body:
                    self.__parse_soup_to_html_text(_soup_body)

    def __parse_soup_to_html_text(self, soup):
        _soup_body = self._clean_soup_useless_tags(soup)
        # print(_soup_body.prettify())

        _soup_phonitic = _soup_body.find_all("span", class_="Phonitic-Sep")
        for _soup in _soup_phonitic:
            self.phonitic_sep = _soup.getText()

        _soup_phonitic = _soup_body.find_all("span", class_="Phonitic")
        for _soup in _soup_phonitic:
            self.phonitic = _soup.getText()

    def _start_parse_type(self, soup):
        # parse type
        _type_desc: str = ''

        _soup_de_type = soup.find_all("span", class_="cara")
        _type_times: int = 0
        for _type in _soup_de_type:
            if _type_times < 1:
                _type_desc = _type.getText()
                _type_times += 1
            else:
                break

        self.type_desc = _type_desc

    def _start_parse_zh(self, soup):
        _word_zh: str = ''
        _soup_zhs = soup.find_all("span", class_="exp")
        # print(_soup_zhs)

        _zh_times: int = 0
        for _zh in _soup_zhs:
            if _zh_times < 2:
                _new_zh = _clean_parenthesis(_zh.getText()).split(',')[0]
                if _zh_times == 0:
                    _word_zh = _new_zh
                else:
                    if _new_zh.find('①') >= 0:
                        _word_zh += _new_zh

                _zh_times += 1
            else:
                break

        self.word.wort_zh = _word_zh

    def get_crawl_result(self):
        self.word.phonitic_sep = self.phonitic_sep
        self.word.phonitic = self.phonitic
        _type_desc = self.type_desc.lower()

        self.word.type = 'n'
        self.word.plural = '-'
        self.word.publish_status = 1
        if _type_desc.find('pl') >= 0:
            self.word.wort_sex = 'Pl.'
        elif _type_desc.find('der') >= 0:
            self.word.wort_sex = 'der'
        elif _type_desc.find('die') >= 0:
            self.word.wort_sex = 'die'
        elif _type_desc.find('das') >= 0:
            self.word.wort_sex = 'das'
        elif _type_desc.find('f,') >= 0:
            self.word.wort_sex = 'die'
        elif _type_desc.find('m,') >= 0:
            self.word.wort_sex = 'der'
        elif _type_desc.find('m.') == 0:
            self.word.wort_sex = 'der'
        else:
            self.word.wort_sex = '-'
            if _type_desc.find('pron') >= 0:
                self.word.type = 'pron'
            elif _type_desc.find('adj') >= 0:
                self.word.type = 'adj'
            elif _type_desc.find('adv') >= 0:
                self.word.type = 'adv'
            elif _type_desc.find('vt') >= 0:
                self.word.type = 'v'
            elif _type_desc.find('vi') >= 0:
                self.word.type = 'v'
            else:
                self.word.type = '?'
                self.word.publish_status = -1
                if _type_desc.find('n.') >= 0:
                    self.word.type = 'n'

        if self.word.type == 'n':
            _type_descs = self.type_desc.split(',')
            if len(_type_descs) > 1:
                self.word.plural = _type_descs[len(_type_descs) - 1]
                self.word.publish_status = 1
        if self.word.wort_zh == '':
            self.word.publish_status = -1

        return self.word, self.url_status, self.type_desc


def _clean_parenthesis(original_string: str) -> str:
    _new_str: str = original_string

    _left_bracket_index = original_string.find('（')
    _right_bracket_index = original_string.find('）')
    if _right_bracket_index > _left_bracket_index:
        _new_str = original_string[:_left_bracket_index]
        _new_str += original_string[_right_bracket_index + 1:]

    return _new_str
