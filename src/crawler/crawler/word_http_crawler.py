from src.crawler.crawler.util.http_request import HttpRequest, HttpUrlRule
from src.service.model.model_content import ContentDictionary


class WordHttpCrawler(HttpRequest):
    phonitic = ''
    phonitic_sep = ''
    type_desc = ''

    def __init__(self, rule: HttpUrlRule, wort: str=None):
        _wort = '' if wort is None else wort
        self.word: ContentDictionary = ContentDictionary(_wort)
        self.word.plural = '-'
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
        _soup_types = soup.find_all("span", class_="cara")
        _type_count = len(_soup_types)

        if _type_count > 0:
            if _type_count > 1:
                _index: int = _choose_type_index(self.word.wort, _soup_types[0].getText(), _soup_types[1].getText())
                _type_desc = _soup_types[_index - 1].getText()
            else:
                _type_desc = _soup_types[0].getText()

        self.type_desc = _type_desc

    def _start_parse_zh(self, soup):
        _word_zh: str = ''
        _soup_zhs = soup.find_all("span", class_="exp")
        if len(_soup_zhs) == 0:
            _soup_zhs = soup.find_all("p", class_="exp")

        _zh_times: int = 0
        for _zh in _soup_zhs:
            if _zh_times < 2:
                _clean_zh = _clean_parenthesis(_zh.getText())
                _clean_zhs = _clean_zh.split(',') if _clean_zh.find(',') > 0 else _clean_zh.split('，')
                _new_zh = _clean_zhs[0]
                print(_new_zh)
                if _zh_times == 0:
                    _word_zh = _new_zh
                else:
                    if _new_zh.find('①') >= 0:
                        _word_zh += _new_zh

                _zh_times += 1
            else:
                break

        if len(_soup_zhs) == 0 and _word_zh == '':
            [s.extract() for s in soup.find_all("span", class_="cara")]
            print(soup.getText().strip())
            _type_desc = soup.getText().strip() if self.type_desc == '' else self.type_desc
            self._start_match_type(_type_desc)
            print(self.word.type)
            _word_zh, self.word.plural = _parse_zh_html(soup.getText(), self.word.type)

        self.word.wort_zh = _word_zh

    def _start_match_type(self, type_desc):
        _type_desc = type_desc.lower()

        self.word.type = 'n'
        self.word.crawl_status = 1
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
        elif _type_desc.find('f.') >= 0:
            self.word.wort_sex = 'die'
        elif _type_desc.find('m,') >= 0:
            self.word.wort_sex = 'der'
        elif _type_desc.find('m.') >= 0:
            self.word.wort_sex = 'der'
        elif _type_desc.find('m;') >= 0:
            self.word.wort_sex = 'der'
        else:
            self.word.type = '?'
            if _type_desc.find('n.') >= 0:
                self.word.type = 'n'
            elif _type_desc.find('n,') >= 0:
                self.word.type = 'n'
            elif _type_desc.find('adj') >= 0:
                self.word.type = 'adj'

    def get_crawl_result(self):

        _type_desc = self.type_desc.lower()
        self._start_match_type(_type_desc)

        if self.word.type == '?':
            self.word.wort_sex = '-'
            self.word.plural = '-'

            if _type_desc.find('pron') >= 0:
                self.word.type = 'pron'
            elif _type_desc.find('adj') >= 0:
                self.word.type = 'adj'
            elif _type_desc.find('adv') >= 0:
                self.word.type = 'adv'
            elif _type_desc.find('konj') >= 0:
                self.word.type = 'konj'
            elif _type_desc.find('vt') >= 0:
                self.word.type = 'v'
            elif _type_desc.find('vi') >= 0:
                self.word.type = 'v'
            else:
                self.word.type = '?'
                self.word.crawl_status = -1

        if self.word.type == 'n' and self.word.plural == '-':
            _type_descs = self.type_desc.split(',')
            if len(_type_descs) > 1:
                self.word.plural = _type_descs[len(_type_descs) - 1]
                self.word.crawl_status = 1

        self.word.crawl_status = -1 if self.word.wort_zh == '' else self.word.crawl_status
        self.word.phonitic_sep = self.phonitic_sep
        self.word.phonitic = self.phonitic
        return self.word, self.url_status, self.type_desc


def _clean_parenthesis(original_string: str) -> str:
    _new_str: str = original_string

    _left_bracket_index = original_string.find('（') if original_string.find('（') > 0 else original_string.find('(')
    _right_bracket_index = original_string.find('）') if original_string.find('）') > 0 else original_string.find(')')

    if _right_bracket_index > _left_bracket_index:
        _new_str = original_string[:_left_bracket_index]
        _new_str += original_string[_right_bracket_index + 1:]

    return _new_str


def _choose_type_index(wort: str, type_1: str, type_2: str) -> int:
    _choose_index: int = 0
    _type_letters = ['der', 'die', 'das', 'm,', 'm.', 'm;', 'n.', 'n,', 'vt', 'vi', 'adj', 'adv']

    if len(type_1) < 3:
        return 2
    else:
        if type_1.find(wort) > 0:
            _choose_index = 2

        _type_1 = type_1.lower()
        for _type in _type_letters:
            if _type_1.find(_type) >= 0:
                _choose_index = 1
                break

        _type_2 = type_2.lower()
        if _choose_index == 0:
            for _type2 in _type_letters:
                if _type_2.find(_type2) >= 0:
                    _choose_index = 2
                    break

        return 1 if _choose_index == 0 else _choose_index


def _parse_zh_html(wort_zh: str, wort_type: str):
    _wort_zh = wort_zh.strip()
    _plural = '-'

    if wort_type == 'n':
        _plural_index = _wort_zh.find(' ')
        _plural = _wort_zh[:_plural_index] if _plural_index > 0 else '-'
        _plural = _plural if len(_plural) < 6 else '-'

    _1_index = wort_zh.find('①')
    _2_index = wort_zh.find('②')
    if _1_index >= 0 and _2_index > 0:
        _wort_zh = wort_zh[_1_index:_2_index]

    _clean_zh = _clean_parenthesis(_wort_zh).strip()
    _clean_zhs = _clean_zh.split(',') if _clean_zh.find(',') > 0 else _clean_zh.split('，')
    _parse_zhs = _clean_zhs[0][_clean_zhs[0].find(' '):] if _clean_zhs[0].find(' ') > 0 else _clean_zhs[0]

    return '' if len(_parse_zhs) > 10 else _parse_zhs, _plural
