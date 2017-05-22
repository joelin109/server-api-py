from flask_restful import Resource, reqparse
from src.service.config import Conf
from src.service.model.model_content import ContentDictionary
from src.service.api.util import api_response_format, api_response_detail_format, api_response_format_err,  api_request_parse
from src.service.logic.dictionary_logic import DictionaryLogic, WordListFilter


class WortApi(Resource):
    def post(self):
        print(reqparse.request.url)
        print(reqparse.request.path)
        _parser = reqparse.RequestParser()
        _request_data = api_request_parse(_parser)

        _post_wort = _get_request_data(_request_data)
        _result = _response_result(_post_wort)
        return _result


class WortListApi(Resource):
    def get(self):
        pass

    def post(self):
        _request_data = api_request_parse()

        _list_filter = _get_request_data_filter(_request_data)
        try:
            _list_filter = _get_request_data_filter(_request_data)
            _logic = DictionaryLogic()
            _result_list, _page = _logic.get_list(_list_filter)
            return api_response_format(_result_list, _page)

        except RuntimeError as ex:
            print(ex)
            return api_response_format_err(str(ex))


def _response_result(_post_wort):
    _logic = DictionaryLogic()
    _word = _logic.get_detail(_post_wort.wort)

    if _word is None:
        _logic.new(_post_wort)
    else:
        _post_wort.id = _word.id
        _logic.update(_post_wort)

    if reqparse.request.path == Conf.APIURL_Content_Dictionary_Remove:
        _logic.delete(_word.first())

    # await asyncio.sleep(2)
    _list, _page = _logic.get_list()
    return api_response_format(_list, _page)


def _get_request_data(request_data):
    new_word = ContentDictionary('')
    new_word.wort = request_data["Word"]
    new_word.wort_sex = request_data["Sex"]
    new_word.level = request_data["Level"]
    new_word.type = request_data["Type"]
    new_word.plural = request_data["Plural"]
    new_word.synonym = request_data["Synonym"]
    new_word.wort_zh = request_data["Word_Zh"]
    new_word.wort_en = request_data["Word_En"]
    new_word.konjugation = request_data["Konjugation"]
    new_word.is_regel = request_data["isRegel"]
    new_word.is_recommend = request_data["isRecommend"]

    print(new_word.wort)
    return new_word


def _get_request_data_filter(request_data):
    if 'filter' in request_data:
        _request_data_filter = request_data["filter"]
        _list_filter = WordListFilter()
        _list_filter.parse(_request_data_filter)
        return _list_filter

    else:
        return None
