from flask_restful import Resource, reqparse
from src.service.config import Conf
from src.service.model.model_content import db, ContentDictionary
from src.service.api.util import api_response_format
from src.service.logic.dictionary_logic import DictionaryLogic
import asyncio
import selectors

loop = asyncio.get_event_loop()


class WortApi(Resource):
    def post(self):
        print(reqparse.request.url)
        print(reqparse.request.path)

        parser = reqparse.RequestParser()
        parser.add_argument('token', type=str, location='json')
        parser.add_argument('data', location='json')
        args = parser.parse_args()

        _token = args['token']
        _data = eval(args['data'])
        _post_wort = _parse_request_data(_data)

        _resut = loop.run_until_complete(_response_result(_post_wort))
        # loop.close()
        return _resut


class WortListApi(Resource):
    def get(self):
        pass

    def post(self):
        _logic = DictionaryLogic()
        _result_list, _page = _logic.get_list()
        return api_response_format(_result_list, _page)


async def _response_result(_post_wort):
    _logic = DictionaryLogic()
    _word = _logic.get_detail(_post_wort.wort)
    if _word is None:
        _logic.new(_post_wort)
    else:
        _post_wort.id = _word.id
        _logic.update_word(_post_wort)

    if reqparse.request.path == Conf.APIURL_Content_Dictionary_Remove:
        db.session.delete(_word.first())
        db.session.commit()

    #await asyncio.sleep(2)
    _list, _page = _logic.get_list()
    return api_response_format(_list, _page)


def _parse_request_data(request_data):
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
