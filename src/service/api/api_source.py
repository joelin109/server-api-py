from flask_restful import Api
from src.service.config import Conf
from src.service.api.user import UserApi
from src.service.api.channel import ChannelApi, ChannelListApi
from src.service.api.article import ArticleApi, ArticleStatusApi, ArticleListApi, ArticleDetailApi
from src.service.api.wort import WortApi, WortListApi
from src.service.api.crawler import CrawlArticleApi, CrawlArticleBodyApi, CrawlHttpURLApi, CrawlWortApi


def register_api_add_resource(app):
    rest_api = Api(app)

    rest_api.add_resource(UserApi, Conf.APIURL_USER_Post, Conf.APIURL_USER_Remove)

    rest_api.add_resource(ChannelApi, Conf.APIURL_Content_Channel_Post)
    rest_api.add_resource(ChannelListApi, Conf.APIURL_Content_Channel_List)
    rest_api.add_resource(ArticleApi, Conf.APIURL_Content_Article_Post)
    rest_api.add_resource(ArticleStatusApi, Conf.APIURL_Content_Article_Status_Update)
    rest_api.add_resource(ArticleListApi, Conf.APIURL_Content_Article_List)
    rest_api.add_resource(ArticleDetailApi, Conf.APIURL_Content_Article_Detail)
    rest_api.add_resource(WortApi, Conf.APIURL_Content_Dictionary_Post, Conf.APIURL_Content_Dictionary_Detail)
    rest_api.add_resource(WortListApi, Conf.APIURL_Content_Dictionary_List)
    rest_api.add_resource(CrawlArticleApi, Conf.APIURL_Content_Crawler_Article)
    rest_api.add_resource(CrawlArticleBodyApi, Conf.APIURL_Content_Crawler_Article_Body)
    rest_api.add_resource(CrawlHttpURLApi, Conf.APIURL_Content_Crawler_Http_URL)
    rest_api.add_resource(CrawlWortApi, Conf.APIURL_Content_Crawler_Word)
