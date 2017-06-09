import os


class SQLConfig(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    file_path = os.path.join(os.path.dirname(__file__) + '/../db/sqlrest.db')
    SQLALCHEMY_DATABASE_SQLLite = 'sqlite:///' + file_path  # 'sqlite:////absolute/path/to/foo.db'
    SQLALCHEMY_DATABASE_MySQL = 'mysql://root:my7678@localhost:3306/joerest'
    SQLALCHEMY_DATABASE_PostgreSQL = 'postgresql://postgres:123456@localhost:5432/sqlrest'
    SQLALCHEMY_DATABASE_PostgreSQL_aws = 'postgresql://postgres:joelin502@aws-postgres.c35dsckzatca.ap-southeast-1.rds.amazonaws.com:5432/api_postgres'
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_PostgreSQL


class Conf(object):
    DEBUG = True
    APIURL_USER_List = '/api/user/list'
    APIURL_USER_Detail = '/api/user/detail'
    APIURL_USER_Post = '/api/user/post'
    APIURL_USER_Remove = '/api/user/remove'

    APIURL_Content_Channel_List = '/api/content/channel/list'
    APIURL_Content_Channel_Post = '/api/content/channel/post'
    APIURL_Content_Article_List = '/api/content/article/list'
    APIURL_Content_Article_Detail = '/api/content/article/detail'
    APIURL_Content_Article_Post = '/api/content/article/post'
    APIURL_Content_Article_Remove = '/api/content/article/remove'
    APIURL_Content_Article_Status_Update = '/api/content/article/status_update'
    APIURL_Content_Dictionary_List = '/api/content/dictionary/list'
    APIURL_Content_Dictionary_Detail = '/api/content/dictionary/detail'
    APIURL_Content_Dictionary_Post = '/api/content/dictionary/post'
    APIURL_Content_Dictionary_Remove = '/api/content/dictionary/remove'
    APIURL_Content_Crawler_Article = '/api/content/crawler/article'
    APIURL_Content_Crawler_Article_Body = '/api/content/crawler/article_body'
    APIURL_Content_Crawler_Http_URL = '/api/content/crawler/http_url'
    APIURL_Content_Crawler_Word = '/api/content/crawler/word'
