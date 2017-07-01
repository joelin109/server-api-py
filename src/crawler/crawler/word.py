from src.crawler.crawler.word_http_crawler import WordHttpCrawler, HttpUrlRule
from src.service.logic.dictionary_logic import DictionaryLogic, WordListFilter


def request_crawl_words(words: str = None):
    _crawl_result: dict = {}
    _crawl_result_rows: list = []

    _list_filter = WordListFilter()
    #_list_filter.page_size = 1
    # _list_filter.word_letter = 's'
    _list_filter.parse()
    _list_filter.filter_sql += ' and publish_status = 0 and zh=\'\''

    _logic = DictionaryLogic()
    _result_list, _page = _logic.get_list(_list_filter)

    try:
        # for _word in _result_list:
        #    _wort = _word['wort']
        for _wort in words.split(','):
            _crawl_word, _crawl_result_row = request_crawl_word(_wort)
            _crawl_result_rows.append(_crawl_result_row)
            # _logic.update_crawl_result(_crawl_word)

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
            "status": _crawl_word.publish_status
        }

        return _crawl_word, _parse_result
