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
    id = Column('UserID', String(32), primary_key=True)
    app_ver = Column('AppVersion', String(50))
    # ios.phone/ios.web
    site_code = Column('SiteCode', String(50))

    account_name = Column('AccountName', String(32), nullable=False, unique=True)
    account_icon = Column('AccountIcon', String(255))
    email = Column('Email', String(50))
    mobile = Column('Mobile', String(50))

    real_name = Column('UserName', String(50), nullable=False)
    gender = Column('Gender', String(50))
    birthday = Column('Birthday', DateTime())
    profile_desc = Column('ProfileDesc', String(255))
    profile_domain = Column('ProfileDomain', String(255))
    region_country = Column('RegionCountry', String(50))
    region_city = Column('RegionCity', String(50))
    create_date = Column('CreateDate', DateTime(), nullable=False, default=datetime.now())
    create_ip = Column('CreateIP', String(50))
    create_device_serial = Column('CreateDeviceSerial', String(50))
    last_access_date = Column('LastAccessDate', DateTime())
    last_access_ip = Column('LastAccessIP', String(50))
    last_access_device_serial = Column('LastAccessDeviceSerial', String(50))
    last_update_date = Column('LastUpdateDate', DateTime())
    valid_status = Column('ValidStatus', SmallInteger(), nullable=False, default=1)

    # wechat/facebook
    certificate_type = Column('CertificateType', String(50))
    certificate_user_id = Column('CertificateAccount', String(50))
    certificate_username = Column('CertificateUserName', String(50))
    certificate_desc = Column('CertificateDesc', String(255))
    certificate_status = Column('CertificateStatus', SmallInteger())
    auth_status = Column('AccountStatus', SmallInteger(), nullable=False, default=0)
    auth_password = Column('AccountPassword', String(50))
    auth_activate_code = Column('AuthActivateCode', String(64))
    auth_activate_date = Column('AuthActivateDate', DateTime())

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
    user_id = Column('UserID', Integer(), primary_key=True)
    token = Column('Token', String(64), primary_key=True)
    account_name = Column('AccountName', String(32))
    app_ver = Column('AppVersion', String(50))

    # token type, such as the access token, refresh token, security token, etc.
    token_type = Column('TokenType', SmallInteger())
    token_expire_date = Column('ExpireDate', DateTime())
    token_valid_status = Column('ValidStatus', SmallInteger())
    create_date = Column('CreateDate', DateTime())
    last_access_date = Column('LastAccessDate', DateTime())
    access_times = Column('AccessTimes', SmallInteger())

    def __init__(self, account):
        self.account_name = account
