from sqlalchemy.inspection import inspect
from datetime import datetime
from src.service.model.db_connection import db, custom_random_key

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


class ContentChannel(db.Model):
    __tablename__ = _table_content_channel_.lower()
    id = db.Column('id', db.String(32), primary_key=True)
    channel_id = db.Column('channel_id', db.String(32), nullable=False, unique=True, index=True)
    channel_title = db.Column('channel_title', db.String(50), nullable=False, )
    channel_desc = db.Column('desc', db.String(255))
    parent_channel_id = db.Column('parent_channel_id', db.String(32))
    channel_level = db.Column('channel_level', db.SmallInteger(), nullable=False)
    display_order = db.Column('display_order', db.SmallInteger(), nullable=False, default=-1)
    valid_status = db.Column('valid_status', db.SmallInteger(), nullable=False, default=1)

    create_date = db.Column('create_date', db.DateTime(), nullable=False, default=datetime.now())
    create_ip = db.Column('create_ip', db.String(50))
    create_user_id = db.Column('create_user_id', db.String(32))
    update_date = db.Column('update_date', db.DateTime(), nullable=False, default=datetime.now())
    update_ip = db.Column('update_ip', db.String(50))
    update_user_id = db.Column('update_user_id', db.String(32))

    def __init__(self):
        self.id = custom_random_key(self, "CC")

    def __repr__(self):
        return "<Post '{}'>".format(self.tag_item_title)

    def parse(self):
        return serialize(self)


class ContentTag(db.Model):
    __tablename__ = _table_content_tag_.lower()
    id = db.Column('tag_id', db.String(32), primary_key=True)
    tag_title = db.Column('tag_title', db.String(50))
    tag_desc = db.Column('desc', db.String(255))
    display_order = db.Column('display_order', db.SmallInteger())
    valid_status = db.Column('valid_status', db.SmallInteger(), nullable=False, default=1)

    create_date = db.Column('create_date', db.DateTime(), nullable=False, default=datetime.now())
    create_ip = db.Column('create_ip', db.String(50))
    create_user_id = db.Column('create_user_id', db.String(32))
    update_date = db.Column('update_date', db.DateTime())
    update_ip = db.Column('update_ip', db.String(50))
    update_user_id = db.Column('update_user_id', db.String(32))

    def __init__(self, title):
        self.tag_title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.tag_title)

    def parse(self):
        return serialize(self)


# 01-12 ?
class ContentArticle(db.Model):
    __tablename__ = _table_content_article_.lower()
    id = db.Column('article_id', db.String(32), primary_key=True)
    cover_id = db.Column('cover_id', db.String(50))
    title = db.Column('title', db.String(50), nullable=False)
    subtitle = db.Column('subtitle', db.String(100))
    # 0/Text - 1/Html - 2/Jason
    format_type = db.Column('format_type', db.SmallInteger, nullable=False, default=0)
    body_text = db.Column('body_text', db.Text())
    desc = db.Column('desc', db.String(255))
    channel_id = db.Column('channel_id', db.String(32), nullable=False, index=True)
    tag_id = db.Column('tag_id', db.String(32), index=True)
    publish_status = db.Column('publish_status', db.SmallInteger(), nullable=False, default=1)
    original_resource = db.Column('original_resource', db.String(50))  # original resource

    create_user_id = db.Column('create_user_id', db.String(32), nullable=False, index=True)
    create_date = db.Column('create_date', db.DateTime(), nullable=False, default=datetime.now())
    create_ip = db.Column('create_ip', db.String(50))
    create_device_serial = db.Column('create_device_serial', db.String(50))
    create_location = db.Column('create_location', db.String(50))
    approve_status = db.Column('approve_status', db.SmallInteger(), nullable=False, default=1)
    approve_user_id = db.Column('approve_user_id', db.String(32))
    approve_date = db.Column('approve_date', db.DateTime())
    last_update_user_id = db.Column('last_update_user_id', db.String(32))
    last_update_ip = db.Column('last_update_ip', db.String(50))
    last_update_date = db.Column('last_update_date', db.DateTime())
    valid_status = db.Column('valid_status', db.SmallInteger(), nullable=False, default=1, index=True)

    def __init__(self, title=None):
        self.id = custom_random_key(self, "CA")
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)

    def parse(self):
        return serialize(self)


class ContentDictionary(db.Model):
    __tablename__ = _table_content_dictionary_de.lower()
    id = db.Column(db.Integer(), primary_key=True)
    wort = db.Column('wort', db.String(32), nullable=False, unique=True)
    wort_sex = db.Column('wort_sex', db.String(10), nullable=False, default='-', index=True)
    plural = db.Column('plural', db.String(32), nullable=False, default='-')
    wort_zh = db.Column('zh', db.String(50))
    wort_en = db.Column('en', db.String(50))
    level = db.Column('level', db.String(10), nullable=False, default='A', index=True)
    type = db.Column('type', db.String(10), nullable=False, default='', index=True)
    synonym = db.Column('synonym', db.String(50))
    konjugation = db.Column('konjugation', db.String(32))
    is_regel = db.Column('is_regel', db.SmallInteger, nullable=False, default=1, index=True)
    is_recommend = db.Column('is_recommend', db.SmallInteger, nullable=False, default=0, index=True)
    is_ignore = db.Column('is_ignore', db.SmallInteger, nullable=False, default=0)
    create_date = db.Column('create_date', db.DateTime(), nullable=False,
                            default=datetime.now())
    update_date = db.Column('update_date', db.DateTime(), nullable=False,
                            default=datetime.now())

    def __init__(self, wort=None):
        self.wort = wort
        self.create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.update_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def parse(self):
        result_row = {
            "word": self.wort,
            "type": self.type,
            "sex": self.wort_sex,
            "plural": self.plural,
            "ch": self.wort_zh,
            "en": self.wort_en,
            "is_regel": self.is_regel,
            "is_recommend": self.is_recommend
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
class ContentComment(db.Model):
    __tablename__ = _table_content_comment_.lower()
    id = db.Column('comment_id', db.String(32), primary_key=True)
    comment_desc = db.Column('comment_desc', db.String(255), nullable=False)
    comment_like_times = db.Column('comment_like_times', db.SmallInteger, nullable=False, default=0)

    reply_user_id = db.Column('reply_user_id', db.String(32))
    create_user_id = db.Column('create_user_id', db.String(32), nullable=False)
    create_date = db.Column('create_date', db.DateTime(), nullable=False, default=datetime.now())
    create_ip = db.Column('create_ip', db.String(50))
    create_device_serial = db.Column('create_device_serial', db.String(50))
    article_id = db.Column('article_id', db.String(32), db.ForeignKey('content_article.article_id'),
                           nullable=False, index=True)
    valid_status = db.Column('valid_status', db.SmallInteger(), nullable=False, default=1, index=True)

    def parse(self):
        return serialize(self)


# 01-12 (Article)
class ContentLike(db.Model):
    __tablename__ = _table_content_like_.lower()
    id = db.Column('like_id', db.String(32), primary_key=True)

    create_user_id = db.Column('create_user_id', db.String(32), nullable=False)
    create_date = db.Column('create_date', db.DateTime(), nullable=False, default=datetime.now())
    create_ip = db.Column('create_ip', db.String(50))
    create_device_serial = db.Column('create_device_serial', db.String(50))
    article_id = db.Column('article_id', db.String(32), db.ForeignKey('content_article.article_id'),
                           nullable=False, index=True)
    valid_status = db.Column('valid_status', db.SmallInteger(), nullable=False, default=1, index=True)

    def parse(self):
        return serialize(self)


# 01-12 ?
class ContentStatisticArticle(db.Model):
    __tablename__ = _table_content_statistic_article.lower()
    id = db.Column('article_id', db.String(32), primary_key=True)
    like_times = db.Column('like_times', db.SmallInteger, nullable=False, default=0)
    comment_times = db.Column('comment_times', db.SmallInteger, nullable=False, default=0)

    favorite_times = db.Column('favorite_times', db.SmallInteger, nullable=False, default=0)
    view_times = db.Column('view_times', db.SmallInteger, nullable=False, default=0)
    unlike_times = db.Column('unlike_times', db.SmallInteger, nullable=False, default=0)
    forward_times = db.Column('forward_times', db.SmallInteger, nullable=False, default=0)
    share_times = db.Column('share_times', db.SmallInteger, nullable=False, default=0)
    create_date = db.Column('create_date', db.DateTime(), nullable=False, default=datetime.now())
    last_update_date = db.Column('last_update_date', db.DateTime())


content_relation_tag = db.Table(
    _table_content_relation_article_tag.lower(),
    db.Column('ArticleID', db.String(32), db.ForeignKey('content_article.article_id'), primary_key=True),
    db.Column('TagID', db.String(32), db.ForeignKey('content_tag.tag_id'), primary_key=True),
    db.Column('CreateDate', db.DateTime(), nullable=False, default=datetime.now()),
    db.Column('CreateUserID', db.String(32), nullable=False),
    db.Column('ValidStatus', db.Integer(), nullable=False, default=1),
    db.Column('LastUpdateDate', db.DateTime())
)

content_relation_account = db.Table(
    _table_content_relation_article_account.lower(),
    db.Column('ArticleID', db.String(32), db.ForeignKey('content_article.article_id'), primary_key=True),
    db.Column('UserID', db.String(32), primary_key=True),
    db.Column('Like', db.SmallInteger, nullable=False, default=0),
    db.Column('Favorite', db.SmallInteger, nullable=False, default=0),
    db.Column('View', db.SmallInteger, nullable=False, default=0),
    db.Column('UnLike', db.SmallInteger, nullable=False, default=0),
    db.Column('Share', db.SmallInteger, nullable=False, default=0),
    db.Column('CreateDate', db.DateTime(), nullable=False, default=datetime.now()),
    db.Column('LastUpdateDate', db.DateTime())
)


def serialize(self):
    return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

