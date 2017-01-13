from sqlalchemy.inspection import inspect
from datetime import datetime
from webapp.server.model.db_connection import db

_table_content_channel_ = "Content_Channel"
_table_content_tag_ = "Content_Tag"
_table_content_article_ = "Content_Article"
_table_content_article_de = "Content_Article_De"
_table_content_dictionary_de = "Content_Dictionary_De"
_table_content_comment_ = "Content_Comment_201701"
_table_content_like_ = "Content_Like_201701"
_table_content_statistic_article = "Content_Statistic_Article"
_table_content_relation_article_tag = "Content_Relation_Article_Tag"
_table_content_relation_article_account = "Content_Relation_Article_Account_201701"


class ContentChannel(db.Model):
    __tablename__ = _table_content_channel_
    id = db.Column('ChannelID', db.String(32), primary_key=True)
    channel_title = db.Column('ChannelTitle', db.String(50))
    channel_desc = db.Column('Desc', db.String(255))
    parent_channel_id = db.Column('ParentChannelID', db.String(32))
    channel_level = db.Column('ChannelLevel', db.SmallInteger(), nullable=False)
    display_order = db.Column('DisplayOrder', db.SmallInteger())
    valid_status = db.Column('ValidStatus', db.SmallInteger(), nullable=False, default=1)

    create_date = db.Column('CreateDate', db.DateTime(), nullable=False, default=datetime.now())
    create_ip = db.Column('CreateIP', db.String(50))
    create_user_id = db.Column('CreateUserID', db.String(32))
    update_date = db.Column('UpdateDate', db.DateTime())
    update_ip = db.Column('UpdateIP', db.String(50))
    update_user_id = db.Column('UpdateUserID', db.String(32))

    def __init__(self):
        self.id = "100010"

    def __repr__(self):
        return "<Post '{}'>".format(self.tag_item_title)

    def parse(self):
        return serialize(self)


class ContentTag(db.Model):
    __tablename__ = _table_content_tag_
    id = db.Column('TagID', db.String(32), primary_key=True)
    tag_title = db.Column('TagTitle', db.String(50))
    tag_desc = db.Column('Desc', db.String(255))
    display_order = db.Column('DisplayOrder', db.SmallInteger())
    valid_status = db.Column('ValidStatus', db.SmallInteger(), nullable=False, default=1)

    create_date = db.Column('CreateDate', db.DateTime(), nullable=False, default=datetime.now())
    create_ip = db.Column('CreateIP', db.String(50))
    create_user_id = db.Column('CreateUserID', db.String(32))
    update_date = db.Column('UpdateDate', db.DateTime())
    update_ip = db.Column('UpdateIP', db.String(50))
    update_user_id = db.Column('UpdateUserID', db.String(32))

    def __init__(self, title):
        self.tag_item_title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.tag_item_title)

    def parse(self):
        return serialize(self)


# 01-12 ?
class ContentArticle(db.Model):
    __tablename__ = _table_content_article_
    id = db.Column('ArticleID', db.String(32), primary_key=True)
    cover_id = db.Column('CoverID', db.String(50))
    title = db.Column('Title', db.String(50), nullable=False)
    subtitle = db.Column('SubTitle', db.String(100))
    # 0/Text - 1/Html - 2/Jason
    format_type = db.Column('FormatType', db.SmallInteger, nullable=False, default=0)
    body_text = db.Column('BodyText', db.Text())
    desc = db.Column('Desc', db.String(255))
    channel_id = db.Column('ChannelID', db.String(32), nullable=False)
    tag_id = db.Column('TagID', db.String(32))
    publish_status = db.Column('PublishStatus', db.SmallInteger(), nullable=False, default=1)
    original_resource = db.Column('OriginalResource', db.String(50))  # original resource

    create_user_id = db.Column('CreateUserID', db.String(32), nullable=False)
    create_date = db.Column('CreateDate', db.DateTime(), nullable=False, default=datetime.now())
    create_ip = db.Column('CreateIP', db.String(50))
    create_device_serial = db.Column('CreateDeviceSerial', db.String(50))
    create_location = db.Column('CreateLocation', db.String(50))
    approve_status = db.Column('ApproveStatus', db.SmallInteger(), nullable=False, default=1)
    approve_user_id = db.Column('ApproveUserID', db.String(32))
    approve_date = db.Column('ApproveDate', db.DateTime())
    last_update_user_id = db.Column('LastUpdateUserID', db.String(32))
    last_update_ip = db.Column('LastUpdateIP', db.String(50))
    last_update_date = db.Column('LastUpdateDate', db.DateTime())
    valid_status = db.Column('ValidStatus', db.SmallInteger(), nullable=False, default=1)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)

    def parse(self):
        return serialize(self)


class ContentDictionary(db.Model):
    __tablename__ = _table_content_dictionary_de
    id = db.Column(db.Integer(), primary_key=True)
    wort = db.Column('Wort', db.String(32), nullable=False, unique=True)
    wort_sex = db.Column('WortSex', db.String(10), nullable=False, default='-')
    plural = db.Column('Plural', db.String(32), nullable=False, default='')
    wort_zh = db.Column('Zh', db.String(50))
    wort_en = db.Column('En', db.String(50))
    level = db.Column('Level', db.String(10), nullable=False, default='A')
    type = db.Column('Type', db.String(10), nullable=False, default='')
    synonym = db.Column('Synonym', db.String(50))
    konjugation = db.Column('Konjugation', db.String(32))
    is_regel = db.Column('IsRegel', db.SmallInteger, nullable=False, default=1)
    is_recommend = db.Column('IsRecommend', db.SmallInteger, nullable=False, default=0)
    is_ignore = db.Column('IsIgnore', db.SmallInteger, nullable=False, default=0)
    create_date = db.Column('CreateDate', db.DateTime(), nullable=False,
                            default=datetime.now())
    update_date = db.Column('UpdateDate', db.DateTime(), nullable=False,
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
            "word_ch": self.wort_zh,
            "word_en": self.wort_en,
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
    __tablename__ = _table_content_comment_
    id = db.Column('CommentID', db.String(32), primary_key=True)
    comment_desc = db.Column('CommentDesc', db.String(255), nullable=False)
    comment_like_times = db.Column('CommentLikeTimes', db.SmallInteger, nullable=False, default=0)

    reply_user_id = db.Column('ReplyUserID', db.String(32))
    create_user_id = db.Column('CreateUserID', db.String(32), nullable=False)
    create_date = db.Column('CreateDate', db.DateTime(), nullable=False, default=datetime.now())
    create_ip = db.Column('CreateIP', db.String(50))
    create_device_serial = db.Column('CreateDeviceSerial', db.String(50))
    article_id = db.Column('ArticleID', db.String(32), db.ForeignKey('Content_Article.ArticleID'), nullable=False)
    valid_status = db.Column('ValidStatus', db.SmallInteger(), nullable=False, default=1)

    def parse(self):
        return serialize(self)


# 01-12 (Article)
class ContentLike(db.Model):
    __tablename__ = _table_content_like_
    id = db.Column('LikeID', db.String(32), primary_key=True)

    create_user_id = db.Column('CreateUserID', db.String(32), nullable=False)
    create_date = db.Column('CreateDate', db.DateTime(), nullable=False, default=datetime.now())
    create_ip = db.Column('CreateIP', db.String(50))
    create_device_serial = db.Column('CreateDeviceSerial', db.String(50))
    article_id = db.Column('ArticleID', db.String(32), db.ForeignKey('Content_Article.ArticleID'), nullable=False)
    valid_status = db.Column('ValidStatus', db.SmallInteger(), nullable=False, default=1)

    def parse(self):
        return serialize(self)


# 01-12 ?
class ContentStatisticArticle(db.Model):
    __tablename__ = _table_content_statistic_article
    id = db.Column('ArticleID', db.String(32), primary_key=True)
    like_times = db.Column('LikeTimes', db.SmallInteger, nullable=False, default=0)
    comment_times = db.Column('CommentTimes', db.SmallInteger, nullable=False, default=0)

    favorite_times = db.Column('FavoriteTimes', db.SmallInteger, nullable=False, default=0)
    view_times = db.Column('ViewTimes', db.SmallInteger, nullable=False, default=0)
    unlike_times = db.Column('UnLikeTimes', db.SmallInteger, nullable=False, default=0)
    forward_times = db.Column('ForwardTimes', db.SmallInteger, nullable=False, default=0)
    share_times = db.Column('ShareTimes', db.SmallInteger, nullable=False, default=0)
    create_date = db.Column('CreateDate', db.DateTime(), nullable=False, default=datetime.now())
    last_update_date = db.Column('LastUpdateDate', db.DateTime())


content_relation_tag = db.Table(
    _table_content_relation_article_tag,
    db.Column('ArticleID', db.String(32), db.ForeignKey('Content_Article.ArticleID'), primary_key=True),
    db.Column('TagID', db.String(32), db.ForeignKey('Content_Tag.TagID'), primary_key=True),
    db.Column('CreateDate', db.DateTime(), nullable=False, default=datetime.now()),
    db.Column('CreateUserID', db.String(32), nullable=False),
    db.Column('ValidStatus', db.Integer(), nullable=False, default=1),
    db.Column('LastUpdateDate', db.DateTime())
)

content_relation_account = db.Table(
    _table_content_relation_article_account,
    db.Column('ArticleID', db.String(32), db.ForeignKey('Content_Article.ArticleID'), primary_key=True),
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
