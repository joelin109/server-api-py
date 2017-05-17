from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, SmallInteger, DateTime, Boolean, ForeignKey
from datetime import datetime
from src.service.model.model import custom_random_key, serialize
from flask_login import AnonymousUserMixin

BaseModel = declarative_base()
_table_account_ = "account_profile"
_table_account_auth_token = "account_auth_token_201701"


class User(BaseModel):
    __tablename__ = _table_account_.lower()
    id = Column('user_id', String(32), primary_key=True)
    app_version = Column('app_version', String(50))
    # ios.phone/ios.web
    site_code = Column('site_code', String(50))

    account_name = Column('account_name', String(32), nullable=False, unique=True)
    account_icon = Column('account_icon', String(255))
    email = Column('email', String(50))
    mobile = Column('mobile', String(50))

    real_user_name = Column('real_user_name', String(50), nullable=False)
    gender = Column('gender', String(50))
    birthday = Column('birthday', DateTime())
    profile_desc = Column('profile_desc', String(255))
    profile_domain = Column('profile_domain', String(255))
    region_country = Column('region_country', String(50))
    region_city = Column('region_city', String(50))
    create_date = Column('create_date', DateTime(), nullable=False, default=datetime.now())
    create_ip = Column('create_ip', String(50))
    create_device_serial = Column('create_device_serial', String(50))
    last_access_date = Column('last_access_date', DateTime())
    last_access_ip = Column('last_access_ip', String(50))
    last_access_device_serial = Column('last_access_device_serial', String(50))
    last_update_date = Column('last_update_date', DateTime())
    valid_status = Column('valid_status', SmallInteger(), nullable=False, default=1)

    # wechat/facebook
    certificate_type = Column('certificate_type', String(50))
    certificate_user_id = Column('certificate_user_id', String(50))
    certificate_username = Column('certificate_username', String(50))
    certificate_desc = Column('certificate_desc', String(255))
    certificate_status = Column('certificate_status', SmallInteger())
    auth_status = Column('auth_status', SmallInteger(), nullable=False, default=0)
    auth_password = Column('auth_password', String(50))
    auth_activate_code = Column('auth_activate_code', String(64))
    auth_activate_date = Column('auth_activate_date', DateTime())

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
class UserAuthToken(BaseModel):
    __tablename__ = _table_account_auth_token.lower()
    user_id = Column('user_id', Integer(), primary_key=True)
    token = Column('token', String(64), primary_key=True)
    account_name = Column('account_name', String(32))
    app_version = Column('app_version', String(50))

    # token type, such as the access token, refresh token, security token, etc.
    token_type = Column('token_type', SmallInteger())
    token_expire_date = Column('token_expire_date', DateTime())
    token_valid_status = Column('token_valid_status', SmallInteger())
    create_date = Column('create_date', DateTime())
    last_access_date = Column('last_access_date', DateTime())
    access_times = Column('access_times', SmallInteger())

    def __init__(self, account):
        self.account_name = account
