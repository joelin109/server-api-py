import requests
from datetime import datetime
from src.service.model.model_content import ContentArticle, ContentTag
from src.service.logic.tag_logic import request_article_tags
from src.service.logic.article_logic import ArticleLogic, ArticleListFilter
from src.crawler.crawler.article_body import request_crawl_article_bodys

crawl_article_url = 'https://newsapi.org/v1/articles'
crawl_article_user_id = 'AP1701yHiCT8v0dnTZm9TR6zJd3A=='
crawl_article_channel_id = ''


def request_crawl_articles():
    _crawl_result = []
    _tag_list = request_article_tags()

    for _tag in _tag_list:
        _crawl_tag = ContentTag(_tag["tag_title"])
        _crawl_tag.tag_id = _tag["tag_id"]
        _crawl_status = 1 if 'is_crawl' not in _tag else _tag['is_crawl']

        if _crawl_status == 1:
            _crawl_count, _crawl_timestamp = request_crawl_tag_articles(_crawl_tag)

            _crawl_result_tag = dict()
            _crawl_result_tag["tag_id"] = _tag["tag_id"]
            _crawl_result_tag["tag_title"] = _tag["tag_title"]
            _crawl_result_tag["crawl_count"] = _crawl_count
            _crawl_result_tag["crawl_timestamp"] = _crawl_timestamp
            _crawl_result.append(_crawl_result_tag)

    return _crawl_result


def request_crawl_tag_articles(crawl_tag):
    _crawl_article_count = 0
    _crawl_tag_id = crawl_tag.tag_id
    _crawl_status, _crawl_result, _crawl_timestamp = _crawl_article_result(crawl_tag)
    print(_crawl_timestamp)

    if _crawl_status:
        _logic = ArticleLogic()
        _top_list = _get_local_crawl_article_list(_crawl_tag_id, _crawl_timestamp)

        for crawl_article in _crawl_result:
            _cover_url = crawl_article["urlToImage"]
            _published_at = crawl_article["publishedAt"]

            if _cover_url is not None and _published_at is not None:
                try:
                    _is_exist = _is_exist_local(_top_list, _published_at)
                    if _is_exist is False:
                        _new_article = _parse_crawl_article(crawl_article, '')
                        _new_article.tag_id = _crawl_tag_id
                        _logic.new(_new_article)
                        _crawl_article_count += 1

                except Exception as ex:
                    print('-------------------------------------   ' + _published_at + '       ---------------')
                    print(str(len(_cover_url)) + '  |   ' + str(len(_new_article.original_url)) + '  |   '
                          + str(len(_new_article.title)) + '  |   ' + str(len(_new_article.desc)))
                    print(str(ex)[0:100])
                    # raise RuntimeError(ex)

    return _crawl_article_count, _crawl_timestamp


def _crawl_article_result(tag):
    _latest_pool = ['der-tagesspiegel', 'the-next-web']
    _crawl_tag_title = tag.tag_title
    _param_order_by = 'latest' if _crawl_tag_title in _latest_pool else 'top'
    _params = {"sortBy": _param_order_by, "source": _crawl_tag_title, "apiKey": 'c53e3bc3f12b4f8ba9b7505d14a4d9f3'}

    _response = requests.get(crawl_article_url, _params)
    _response_status = _response.status_code
    _response_json = _response.json()
    _timestamp = ''

    if _response_status == 200:
        _results = _response_json["articles"]
        _result_count = len(_results)
        if _result_count >= 4:
            _published_at = _results[_result_count - 1]["publishedAt"]
            _timestamp = _published_at if _published_at is not None else _results[_result_count - 2]["publishedAt"]

        _timestamp = datetime.now().strftime('%Y-%m-%d %H:%M') if _timestamp is None or _timestamp == '' else _timestamp
        return True, _results, _timestamp[0:10] + ' 00:00:00'

    else:
        return False, _response_status, _timestamp


def _get_local_crawl_article_list(tag_id=None, published_at=None):
    _logic = ArticleLogic()
    _list = _logic.get_top_list(tag_id, published_at)
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
