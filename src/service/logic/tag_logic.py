import json
from src.service.model.model_content import ContentTag

tag_list = []
tag_dict = {}


def request_article_tags():
    with open('src/sql_static_data.json', encoding='utf-8') as json_file:
        _json_data = json.loads(json_file.read())
        _result_tags = _json_data['result']['tags']

    print(_result_tags)
    return _result_tags
