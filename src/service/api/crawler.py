from flask_restful import Resource, reqparse
from src.service.config import Conf
from src.service.api.util import api_request_parse, api_response_format, api_response_detail_format
from src.crawler.crawler.article import request_crawl_articles, request_crawl_articles_body
from src.crawler.crawler.article_body import crawl_http_url
from src.crawler.crawler.word import request_crawl_words


class CrawlArticleApi(Resource):
    def post(self):
        print(reqparse.request.path)
        _parser = reqparse.RequestParser()
        _request_data = api_request_parse(_parser)

        _result = request_crawl_articles()
        return api_response_format(_result)


class CrawlArticleBodyApi(Resource):
    def post(self):
        print(reqparse.request.path)
        _parser = reqparse.RequestParser()
        _request_data = api_request_parse(_parser)

        request_crawl_articles_body()
        return _request_data


class CrawlHttpURLApi(Resource):
    def post(self):
        print(reqparse.request.path)
        _parser = reqparse.RequestParser()
        _request_data = api_request_parse(_parser)

        _article_id = _request_data["id"]
        _crawl_http_url = _request_data['original_url']

        _result = dict()
        _result["id"] = _article_id
        _result["original_url"] = _crawl_http_url
        _result["body_text"] = crawl_http_url(_crawl_http_url)

        return api_response_detail_format(_result)


class CrawlWortApi(Resource):
    def post(self):
        _request_data = api_request_parse()
        print('request_data:', _request_data)

        _result = request_crawl_words(_request_data["Word"])
        return api_response_detail_format(_result)
