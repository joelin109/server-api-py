from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, String, Integer, SmallInteger, DateTime, Boolean, Text, ForeignKey
from datetime import datetime
from src.service.model.model import custom_random_key, serialize

BaseModel = declarative_base()

_table_content_channel_ = "content_channel"
_table_content_tag_ = "content_tag"
_table_content_article_ = "content_article"
_table_content_article_de = "content_article_de"
_table_content_dictionary_de = "content_dictionary_de"
_table_content_comment_ = "content_comment_201701"
_table_content_like_ = "content_Like_201701"
_table_content_statistic_article = "content_statistic_article"
_table_content_relation_article_tag = "content_relation_article_tag"
_table_content_relation_article_account = "content_relation_article_account_201701"


class ContentChannel(BaseModel):
    __tablename__ = _table_content_channel_.lower()
    id = Column('id', String(32), primary_key=True)
    channel_id = Column('channel_id', String(32), nullable=False, unique=True, index=True)
    channel_title = Column('channel_title', String(50), nullable=False, )
    channel_desc = Column('desc', String(255))
    parent_channel_id = Column('parent_channel_id', String(32))
    channel_level = Column('channel_level', SmallInteger(), nullable=False)
    display_order = Column('display_order', SmallInteger(), nullable=False, default=-1)
    valid_status = Column('valid_status', SmallInteger(), nullable=False, default=1)

    create_date = Column('create_date', DateTime(), nullable=False, default=datetime.now())
    create_ip = Column('create_ip', String(50))
    create_user_id = Column('create_user_id', String(32))
    last_update_date = Column('last_update_date', DateTime(), nullable=False, default=datetime.now())
    last_update_ip = Column('last_update_ip', String(50))
    last_update_user_id = Column('last_update_user_id', String(32))

    def __init__(self):
        self.id = custom_random_key(self, "CC")

    def __repr__(self):
        return "<Post '{}'>".format(self.tag_item_title)

    def parse(self):
        return serialize(self)


class ContentTag(BaseModel):
    __tablename__ = _table_content_tag_.lower()
    id = Column('id', String(32), primary_key=True)
    tag_id = Column('tag_id', String(32), nullable=False, unique=True, index=True)
    tag_title = Column('tag_title', String(50))
    tag_desc = Column('desc', String(255))
    display_order = Column('display_order', SmallInteger())
    valid_status = Column('valid_status', SmallInteger(), nullable=False, default=1)

    create_date = Column('create_date', DateTime(), nullable=False, default=datetime.now())
    create_ip = Column('create_ip', String(50))
    create_user_id = Column('create_user_id', String(32))
    last_update_date = Column('last_update_date', DateTime())
    last_update_ip = Column('last_update_ip', String(50))
    last_update_user_id = Column('last_update_user_id', String(32))

    def __init__(self, title):
        self.tag_title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.tag_title)

    def parse(self):
        return serialize(self)


# 01-12 ?
class ContentArticle(BaseModel):
    __tablename__ = _table_content_article_.lower()

    id = Column('article_id', String(32), primary_key=True)
    cover_thumbnail_src = Column('cover_thumbnail_src', String(200))
    cover_src = Column('cover_src', String(200))
    title = Column('title', String(150), nullable=False, index=True)
    subtitle = Column('subtitle', String(150))
    # 0 (None) - 1/Html - 2/Markdown - 3/JSon - 4/Text
    format_type = Column('format_type', SmallInteger, nullable=False, default=0)
    body_text = Column('body_text', Text())
    body_match_level = Column('body_match_level', SmallInteger(), nullable=False, default=0, index=True)
    desc = Column('desc', String(255))
    channel_id = Column('channel_id', String(32), index=True)
    tag_id = Column('tag_id', String(32), index=True)
    original_url = Column('original_url', String(200))  # original resource
    original_author = Column('original_author', String(50))  # original author

    is_original = Column('is_original', Boolean(), nullable=False, default=False)
    create_user_id = Column('create_user_id', String(32), nullable=False, index=True)
    create_date = Column('create_date', DateTime(), nullable=False, default=datetime.now())
    create_ip = Column('create_ip', String(50))
    create_device_serial = Column('create_device_serial', String(50))
    create_location = Column('create_location', String(50))
    approve_status = Column('approve_status', SmallInteger(), nullable=False, default=1)
    approve_user_id = Column('approve_user_id', String(32))
    approve_date = Column('approve_date', DateTime())
    last_update_user_id = Column('last_update_user_id', String(32))
    last_update_ip = Column('last_update_ip', String(50))
    last_update_date = Column('last_update_date', DateTime(), nullable=False, unique=True, index=True)
    valid_status = Column('valid_status', SmallInteger(), nullable=False, default=1, index=True)

    publish_at = Column('publish_at', String(50), nullable=False, default=0, index=True)
    publish_status = Column('publish_status', SmallInteger(), nullable=False, default=0, index=True)
    is_recommend = Column('is_recommend', Boolean(), nullable=False, default=False, index=True)

    def __init__(self, title=None):
        self.id = custom_random_key(self, "CA")
        self.create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)

    def parse(self):
        result_row = {
            "id": self.id,
            "cover_thumbnail_src": self.cover_thumbnail_src,
            "cover_src": self.cover_src,
            "title": self.title,
            "subtitle": self.subtitle,
            "original_url": self.original_url,
            "desc": self.desc,
            "format_type": self.format_type,
            "body_match_level": self.body_match_level,
            "channel_id": self.channel_id,
            "tag_id": self.tag_id,
            "publish_at": self.publish_at,
            "last_update_date": self.last_update_date.strftime('%Y-%m-%d %H:%M:%S'),
            "is_recommend": self.is_recommend,
            "publish_status": self.publish_status
        }
        return result_row

    def parse_top(self):
        result_row = {
            "id": self.id,
            "cover_thumbnail_src": self.cover_thumbnail_src,
            "title": self.title,
            "original_url": self.original_url,
            "tag_id": self.tag_id,
            "publish_at": self.publish_at,
            "last_update_date": self.last_update_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        return result_row

    def parse_detail(self):
        result_row = {
            "id": self.id,
            "cover_thumbnail_src": self.cover_thumbnail_src,
            "cover_src": self.cover_src,
            "title": self.title,
            "subtitle": self.subtitle,
            "original_url": self.original_url,
            "desc": self.desc,
            "channel_id": self.channel_id,
            "tag_id": self.tag_id,
            "publish_at": self.publish_at,
            "last_update_date": self.last_update_date.strftime('%Y-%m-%d %H:%M:%S'),
            "is_recommend": self.is_recommend,
            "publish_status": self.publish_status,
            "format_type": self.format_type,
            "body_text": self.body_text,
            "body_match_level": self.body_match_level
        }
        return result_row


class ContentDictionary(BaseModel):
    __tablename__ = _table_content_dictionary_de.lower()
    id = Column(Integer(), primary_key=True)
    wort = Column('wort', String(32), nullable=False, unique=True)
    wort_sex = Column('wort_sex', String(10), nullable=False, default='-', index=True)
    phonitic_sep = Column('phonitic_sep', String(32), default='')
    phonitic = Column('phonitic', String(32), default='')
    plural = Column('plural', String(32), nullable=False, default='-')
    wort_zh = Column('zh', String(50), nullable=False, default='')
    wort_en = Column('en', String(50))
    level = Column('level', String(10), nullable=False, default='A', index=True)
    type = Column('type', String(10), nullable=False, default='', index=True)
    synonym = Column('synonym', String(50))
    konjugation = Column('konjugation', String(32))
    is_regel = Column('is_regel', SmallInteger, nullable=False, default=1, index=True)
    is_recommend = Column('is_recommend', SmallInteger, nullable=False, default=0, index=True)
    is_ignore = Column('is_ignore', SmallInteger, nullable=False, default=0)
    create_date = Column('create_date', DateTime(), nullable=False, default=datetime.now())
    last_update_date = Column('last_update_date', DateTime(), nullable=False, default=datetime.now())
    # -1, 0, 1, 2
    publish_status = Column('publish_status', SmallInteger(), nullable=False, default=0, index=True)

    def __init__(self, wort=None):
        self.wort = wort
        self.wort_zh = ''
        self.create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.update_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def parse(self):
        result_row = {
            "id": self.id,
            "wort": self.wort,
            "phonitic": self.phonitic,
            "wort_sex": self.wort_sex,
            "plural": self.plural,
            "zh": self.wort_zh,
            "en": self.wort_en,
            "level": self.level,
            "type": self.type,
            "is_regel": self.is_regel,
            "is_recommend": self.is_recommend,
            "status": self.publish_status,
            "create_date": self.last_update_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        return result_row

    def parse_detail(self):
        result_row = {
            "word": self.wort,
            "type": self.type,
            "sex": self.wort_sex,
            "plural": self.plural,
            "word_ch": self.wort_zh,
            "level": self.level,
        }
        return result_row


# 01-12 (Article)
class ContentComment(BaseModel):
    __tablename__ = _table_content_comment_.lower()
    id = Column('comment_id', String(32), primary_key=True)
    comment_desc = Column('comment_desc', String(255), nullable=False)
    comment_like_times = Column('comment_like_times', SmallInteger, nullable=False, default=0)

    reply_user_id = Column('reply_user_id', String(32))
    create_user_id = Column('create_user_id', String(32), nullable=False)
    create_date = Column('create_date', DateTime(), nullable=False, default=datetime.now())
    create_ip = Column('create_ip', String(50))
    create_device_serial = Column('create_device_serial', String(50))
    article_id = Column('article_id', String(32), ForeignKey('content_article.article_id'), nullable=False, index=True)
    valid_status = Column('valid_status', SmallInteger(), nullable=False, default=1, index=True)

    def parse(self):
        return serialize(self)


# 01-12 (Article)
class ContentLike(BaseModel):
    __tablename__ = _table_content_like_.lower()
    id = Column('like_id', String(32), primary_key=True)

    create_user_id = Column('create_user_id', String(32), nullable=False)
    create_date = Column('create_date', DateTime(), nullable=False, default=datetime.now())
    create_ip = Column('create_ip', String(50))
    create_device_serial = Column('create_device_serial', String(50))
    article_id = Column('article_id', String(32), ForeignKey('content_article.article_id'), nullable=False, index=True)
    valid_status = Column('valid_status', SmallInteger(), nullable=False, default=1, index=True)

    def parse(self):
        return serialize(self)


# 01-12 ?
class ContentStatisticArticle(BaseModel):
    __tablename__ = _table_content_statistic_article.lower()
    id = Column('article_id', String(32), primary_key=True)
    like_times = Column('like_times', SmallInteger, nullable=False, default=0)
    comment_times = Column('comment_times', SmallInteger, nullable=False, default=0)

    favorite_times = Column('favorite_times', SmallInteger, nullable=False, default=0)
    view_times = Column('view_times', SmallInteger, nullable=False, default=0)
    unlike_times = Column('unlike_times', SmallInteger, nullable=False, default=0)
    forward_times = Column('forward_times', SmallInteger, nullable=False, default=0)
    share_times = Column('share_times', SmallInteger, nullable=False, default=0)
    create_date = Column('create_date', DateTime(), nullable=False, default=datetime.now())
    last_update_date = Column('last_update_date', DateTime())


content_relation_tag = Table(
    _table_content_relation_article_tag.lower(), BaseModel.metadata,
    Column('article_id', String(32), ForeignKey('content_article.article_id'), primary_key=True),
    Column('tag_id', String(32), ForeignKey('content_tag.tag_id'), primary_key=True),
    Column('create_date', DateTime(), nullable=False, default=datetime.now()),
    Column('create_user_id', String(32), nullable=False),
    Column('valid_status', Integer(), nullable=False, default=1),
    Column('last_update_date', DateTime())
)

content_relation_account = Table(
    _table_content_relation_article_account.lower(), BaseModel.metadata,
    Column('article_id', String(32), ForeignKey("content_article.article_id"), primary_key=True),
    Column('user_id', String(32), primary_key=True),
    Column('like', SmallInteger, nullable=False, default=0),
    Column('favorite', SmallInteger, nullable=False, default=0),
    Column('view', SmallInteger, nullable=False, default=0),
    Column('unlike', SmallInteger, nullable=False, default=0),
    Column('share', SmallInteger, nullable=False, default=0),
    Column('create_date', DateTime(), nullable=False, default=datetime.now()),
    Column('last_update_date', DateTime())
)

