import requests
from src.service.model.model_content import db, ContentArticle
from src.service.logic.article_logic import ArticleLogic, ArticleListFilter
from src.service.crawler.article_body import request_crawl_article_bodys
from datetime import datetime

crawl_article_url = 'https://newsapi.org/v1/articles'
crawl_article_user_id = 'AP1701yHiCT8v0dnTZm9TR6zJd3A=='
crawl_article_channel_id = ''


def request_crawl_articles():
    _crawl_article_count = 0
    _tag = {}
    _crawl_status, _crawl_result, _crawl_publish_at = _crawl_article_result(_tag)
    print(_crawl_publish_at)

    if _crawl_status:
        _logic = ArticleLogic()
        _top_list = _get_local_crawl_article_list(_tag, _crawl_publish_at)

        for crawl_article in _crawl_result:
            _cover_url = crawl_article["urlToImage"]
            _published_at = crawl_article["publishedAt"]

            if _cover_url is not None and _published_at is not None:
                try:
                    _is_exist = _is_exist_local(_top_list, _published_at)
                    if _is_exist is False:
                        _new_article = _parse_crawl_article(crawl_article, '')
                        _logic.new(_new_article)
                        _crawl_article_count += 1

                except Exception as ex:
                    print(_cover_url + '   |   ' + str(len(_cover_url)) + '  |   ' + _published_at)
                    print(ex)
                    # raise RuntimeError(ex)

    print(str(_crawl_article_count))
    return _top_list


def _crawl_article_result(tag):
    _params = {"sortBy": 'top', "source": 'entertainment-weekly', "apiKey": 'c53e3bc3f12b4f8ba9b7505d14a4d9f3'}
    _response = requests.get(crawl_article_url, _params)
    _response_status = _response.status_code
    _response_json = _response.json()
    _publish_at = ''

    if _response_status == 200:
        _results = _response_json["articles"]
        _result_count = len(_results)
        if _result_count >= 6:
            _published_at = _results[_result_count - 3]["publishedAt"]
            _publish_at = _published_at if _published_at is not None else _results[_result_count - 2]["publishedAt"]

        _publish_at = _publish_at[0:10] + ' 00:00:00' if _publish_at is not None else ''
        return True, _results, _publish_at

    else:
        return False, _response_status, _publish_at


def _get_local_crawl_article_list(tag=None, published_at=None):
    _logic = ArticleLogic()
    _list = _logic.get_top_list(published_at)
    return _list


def _is_exist_local(local_list, publish_at):
    for local_article in local_list:
        if publish_at == local_article["publish_at"]:
            return True

    return False


def _is_exist_local_publish_at(local_publish_at_list, publish_at):
    _is_exist = publish_at in local_publish_at_list
    return _is_exist


def _parse_crawl_article(crawl_article, tag_id=None):
    _publish_at = crawl_article["publishedAt"]

    _article = ContentArticle('')
    _article.title = crawl_article["title"]
    _article.cover_thumbnail_src = crawl_article["urlToImage"]
    _article.desc = crawl_article["description"]
    _article.original_url = crawl_article["url"]
    _article.original_author = crawl_article["author"]
    _article.publish_at = _publish_at

    _article.create_user_id = crawl_article_user_id
    _article.channel_id = crawl_article_channel_id
    _article.tag_id = '' if tag_id is None else tag_id
    _article.last_update_date = _publish_at.replace("T", " ").replace("Z", " ")

    return _article


def request_crawl_articles_body():
    request_crawl_article_bodys()
    return ''
