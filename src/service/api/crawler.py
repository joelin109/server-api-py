from flask_restful import Resource, reqparse
from src.service.config import Conf
from src.service.api.util import api_response_format, api_request_parse
from src.service.crawler.article import request_crawl_articles, request_crawl_articles_body


class CrawlerApi(Resource):
    def post(self):
        print(reqparse.request.path)
        _parser = reqparse.RequestParser()
        _request_data = api_request_parse(_parser)

        _result = request_crawl_articles()
        return api_response_format(_result)


class CrawlerBodyApi(Resource):
    def post(self):
        print(reqparse.request.path)
        _parser = reqparse.RequestParser()
        _request_data = api_request_parse(_parser)

        request_crawl_articles_body()
        return _request_data
