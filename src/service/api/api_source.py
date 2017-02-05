from flask_restful import Api
from src.service.config import APIConfig
from src.service.api.user import UserApi
from src.service.api.channel import ChannelApi, ChannelListApi
from src.service.api.article import ArticleApi, ArticleListApi
from src.service.api.wort import WortApi, WortListApi


def register_api_add_resource(app):
    rest_api = Api(app)

    rest_api.add_resource(UserApi, APIConfig.APIURL_USER_Post, APIConfig.APIURL_USER_Remove)

    rest_api.add_resource(ChannelApi, APIConfig.APIURL_Content_Channel_Post)
    rest_api.add_resource(ChannelListApi, APIConfig.APIURL_Content_Channel_List)
    rest_api.add_resource(ArticleApi, APIConfig.APIURL_Content_Article_Post, APIConfig.APIURL_Content_Article_Detail)
    rest_api.add_resource(ArticleListApi, APIConfig.APIURL_Content_Article_List)
    rest_api.add_resource(WortApi, APIConfig.APIURL_Content_Dictionary_Post, APIConfig.APIURL_Content_Dictionary_Detail)
    rest_api.add_resource(WortListApi, APIConfig.APIURL_Content_Dictionary_List)
