from flask_restful import Resource, reqparse
from webapp.service.config import APIConfig
from webapp.service.model.model_content import db, ContentDictionary
from webapp.service.api.util import api_result
from webapp.service.logic.dictionary_handler import DictionaryHandler
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
        pass


async def _response_result(_post_wort):
    _handler = DictionaryHandler()
    _word = _handler.word_detail(_post_wort.wort)
    if _word is None:
        _handler.word_new(_post_wort)
    else:
        _post_wort.id = _word.id
        _handler.word_update(_post_wort)

    if reqparse.request.path == APIConfig.APIURL_Content_Dictionary_Remove:
        db.session.delete(_word.first())
        db.session.commit()

    #await asyncio.sleep(2)

    _list, _page = _handler.word_list("")
    return api_result(_list, _page)


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
