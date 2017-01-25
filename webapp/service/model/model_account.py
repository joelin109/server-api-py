from sqlalchemy.inspection import inspect
from flask_login import AnonymousUserMixin
from datetime import datetime
from webapp.service.model.db_connection import db, custom_random_key


_table_account_ = "account_profile"
_table_account_auth_token = "account_auth_token_201701"


class User(db.Model):
    __tablename__ = _table_account_.lower()
    id = db.Column('UserID', db.String(32), primary_key=True)
    app_ver = db.Column('AppVersion', db.String(50))
    # ios.phone/ios.web
    site_code = db.Column('SiteCode', db.String(50))

    account_name = db.Column('AccountName', db.String(32), nullable=False, unique=True)
    account_icon = db.Column('AccountIcon', db.String(255))
    email = db.Column('Email', db.String(50))
    mobile = db.Column('Mobile', db.String(50))

    real_name = db.Column('UserName', db.String(50), nullable=False)
    gender = db.Column('Gender', db.String(50))
    birthday = db.Column('Birthday', db.DateTime())
    profile_desc = db.Column('ProfileDesc', db.String(255))
    profile_domain = db.Column('ProfileDomain', db.String(255))
    region_country = db.Column('RegionCountry', db.String(50))
    region_city = db.Column('RegionCity', db.String(50))
    create_date = db.Column('CreateDate', db.DateTime(), nullable=False, default=datetime.now())
    create_ip = db.Column('CreateIP', db.String(50))
    create_device_serial = db.Column('CreateDeviceSerial', db.String(50))
    last_access_date = db.Column('LastAccessDate', db.DateTime())
    last_access_ip = db.Column('LastAccessIP', db.String(50))
    last_access_device_serial = db.Column('LastAccessDeviceSerial', db.String(50))
    last_update_date = db.Column('LastUpdateDate', db.DateTime())
    valid_status = db.Column('ValidStatus', db.SmallInteger(), nullable=False, default=1)

    # wechat/facebook
    certificate_type = db.Column('CertificateType', db.String(50))
    certificate_user_id = db.Column('CertificateAccount', db.String(50))
    certificate_username = db.Column('CertificateUserName', db.String(50))
    certificate_desc = db.Column('CertificateDesc', db.String(255))
    certificate_status = db.Column('CertificateStatus', db.SmallInteger())
    auth_status = db.Column('AccountStatus', db.SmallInteger(), nullable=False, default=0)
    auth_password = db.Column('AccountPassword', db.String(50))
    auth_activate_code = db.Column('AuthActivateCode', db.String(64))
    auth_activate_date = db.Column('AuthActivateDate', db.DateTime())

    def __init__(self, account=None):
        self.id = custom_random_key(self, "AP")
        self.account_name = account

    def parse(self):
        return serialize(self)

    # 一般而言，这个方法应该只返回 True，除非表示用户的对象因为某些原因不允许被认证。
    def is_authenticated(self):
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    # is_anonymous方法：为那些不被获准登录的用户返回True。
    def is_anonymous(self):
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    # 应该返回 True，除非用户是无效的，比如他们的账号被禁止。
    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)


# 01-12
class UserAuthToken(db.Model):
    __tablename__ = _table_account_auth_token.lower()
    user_id = db.Column('UserID', db.Integer(), primary_key=True)
    token = db.Column('Token', db.String(64), primary_key=True)
    account_name = db.Column('AccountName', db.String(32))
    app_ver = db.Column('AppVersion', db.String(50))

    # token type, such as the access token, refresh token, security token, etc.
    token_type = db.Column('TokenType', db.SmallInteger())
    token_expire_date = db.Column('ExpireDate', db.DateTime())
    token_valid_status = db.Column('ValidStatus', db.SmallInteger())
    create_date = db.Column('CreateDate', db.DateTime())
    last_access_date = db.Column('LastAccessDate', db.DateTime())
    access_times = db.Column('AccessTimes', db.SmallInteger())

    def __init__(self, account):
        self.account_name = account


def serialize(self):
    return {c: getattr(self, c) for c in inspect(self).attrs.keys()}
