from sqlalchemy.inspection import inspect
from datetime import datetime
from base64 import b64encode
from os import urandom


def serialize(self):
    return {c: getattr(self, c) for c in inspect(self).attrs.keys()}


def custom_random_key(self, table_tag=None):
    random_bytes = urandom(18)
    _key = datetime.now().strftime('%y%m') + b64encode(random_bytes).decode('utf-8')
    _key = _key if table_tag is None else table_tag + _key

    _key_32 = _key if len(_key) <= 32 else _key[0:32]
    return _key_32
