import os


class SQLConfig(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    file_path = os.path.join(os.path.dirname(__file__) + '/../db/sqlrest.db')
    SQLALCHEMY_DATABASE_SQLLite = 'sqlite:///' + file_path  # 'sqlite:////absolute/path/to/foo.db'
    SQLALCHEMY_DATABASE_MySQL = 'mysql://root:my7678@localhost:3306/joerest'
    SQLALCHEMY_DATABASE_PostgreSQL = 'postgresql://postgres:123456@localhost:5432/sqlrest'
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_PostgreSQL


class APIConfig(object):
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
    APIURL_Content_Dictionary_List = '/api/content/dictionary/list'
    APIURL_Content_Dictionary_Detail = '/api/content/dictionary/detail'
    APIURL_Content_Dictionary_Post = '/api/content/dictionary/post'
    APIURL_Content_Dictionary_Remove = '/api/content/dictionary/remove'