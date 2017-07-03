from src.crawler.crawler.word_http_crawler import WordHttpCrawler, HttpUrlRule
from src.service.logic.dictionary_logic import DictionaryLogic, WordListFilter


def request_crawl_words(filter_data: dict = None, will_update_db: bool = False):
    _crawl_result: dict = {}
    _crawl_result_rows: list = []

    _list_filter = WordListFilter()
    _list_filter.parse(filter_data)
    _list_filter.filter_sql += ' and publish_status < 1'

    _logic = DictionaryLogic()
    _result_list, _page = _logic.get_list(_list_filter)

    try:
        _update_db: bool = True if filter_data['update_db'] == 1 else False if 'update_db' in filter_data else False
        _update_level: int = filter_data['update_level'] if 'update_db' in filter_data else 1
        _words = filter_data['wort'] if 'wort' in filter_data else ''

        _list = _result_list if _update_db is True else _words.split(',')
        for _word in _list:
            _wort = _word['wort'] if 'wort' in _word else _word

            _crawl_word, _crawl_result_row = request_crawl_word(_wort)
            _crawl_result_rows.append(_crawl_result_row)

            if _crawl_word.crawl_status >= _update_level:
                _logic.update_crawl_result(_crawl_word)

    except NameError as ex:
        print(ex)

    _crawl_result["rows"] = _crawl_result_rows
    return _crawl_result


def request_crawl_word(wort):
    _url = 'https://www.godic.net/dicts/de/%s' % wort
    _rule = HttpUrlRule(_url)
    _rule.display()

    if _rule.html_parse_body_tag == '':
        return 'Please set parse rule first'
    else:
        _crawler = WordHttpCrawler(_rule, wort)
        _crawler.start()
        _crawl_word, _status, _desc= _crawler.get_crawl_result()

        _parse_result = {
            "type_desc": _desc,
            "wort:": _crawl_word.wort,
            "phonitic_sep": _crawl_word.phonitic_sep,
            "phonitic": _crawl_word.phonitic,
            "wort_sex": _crawl_word.wort_sex,
            "plural": _crawl_word.plural,
            "zh": _crawl_word.wort_zh,
            "type": _crawl_word.type,
            "crawl_status": _crawl_word.crawl_status
        }

        return _crawl_word, _parse_result
