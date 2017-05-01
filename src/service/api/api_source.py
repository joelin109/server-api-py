from flask_restful import Api
from src.service.config import Conf
from src.service.api.user import UserApi
from src.service.api.channel import ChannelApi, ChannelListApi
from src.service.api.article import ArticleApi, ArticleStatusApi, ArticleListApi
from src.service.api.wort import WortApi, WortListApi
from src.service.api.crawler import CrawlerArticleApi, CrawlerArticleBodyApi


def register_api_add_resource(app):
    rest_api = Api(app)

    rest_api.add_resource(UserApi, Conf.APIURL_USER_Post, Conf.APIURL_USER_Remove)

    rest_api.add_resource(ChannelApi, Conf.APIURL_Content_Channel_Post)
    rest_api.add_resource(ChannelListApi, Conf.APIURL_Content_Channel_List)
    rest_api.add_resource(ArticleApi, Conf.APIURL_Content_Article_Post, Conf.APIURL_Content_Article_Detail)
    rest_api.add_resource(ArticleStatusApi, Conf.APIURL_Content_Article_Status_Update)
    rest_api.add_resource(ArticleListApi, Conf.APIURL_Content_Article_List)
    rest_api.add_resource(WortApi, Conf.APIURL_Content_Dictionary_Post, Conf.APIURL_Content_Dictionary_Detail)
    rest_api.add_resource(WortListApi, Conf.APIURL_Content_Dictionary_List)
    rest_api.add_resource(CrawlerArticleApi, Conf.APIURL_Content_Crawler_Article)
    rest_api.add_resource(CrawlerArticleBodyApi, Conf.APIURL_Content_Crawler_Article_Body)
