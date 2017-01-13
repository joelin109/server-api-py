from sqlalchemy.inspection import inspect
from datetime import datetime
from webapp.server.model.db_connection import db

_table_account_ = "Account_Profile"
_table_account_auth_token = "Account_Auth_Token_201701"


class User(db.Model):
    __tablename__ = _table_account_
    user_id = db.Column('UserID', db.String(32), primary_key=True)
    app_ver = db.Column('AppVersion', db.String(50))
    # ios.phone/ios.web
    site_code = db.Column('SiteCode', db.String(50))

    account_name = db.Column('AccountName', db.String(32), nullable=False, unique=True)
    account_icon = db.Column('AccountIcon', db.String(255))
    email = db.Column('Email', db.String(50))
    mobile = db.Column('Mobile', db.String(50))

    username = db.Column('UserName', db.String(50), nullable=False)
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

    def __init__(self, account):
        self.account_name = account

    def __repr__(self):
        # formats what is shown in the shell when print is
        # called on it
        return '<User {}>'.format(self.username)

    def parse(self):
        return serialize(self)


# 01-12
class UserAuthToken(db.Model):
    __tablename__ = _table_account_auth_token
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
