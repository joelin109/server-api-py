import boto3
import requests
import io
from PIL import Image
from datetime import datetime

ACCESS_KEY_ID = 'AKIAJWJDPKGTHBNSWG2Q'
ACCESS_SECRET_KEY = ''


class AwsS3(object):
    client = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_SECRET_KEY)
    type = 'image/jpeg'
    bucket_name = 'i518'
    bucket_folder_name = 'files/img/'
    key = ''
    width, height = 0, 0

    def __init__(self, bucket_name=None, bucket_folder_name=None):
        if bucket_name is not None:
            self.bucket_name = bucket_name

        if bucket_folder_name is not None:
            self.bucket_folder_name = bucket_folder_name

    def upload_local_image(self, img_path, key=None):
        self.key = '' if key is None else key

        _img_data = Image.open(img_path)
        return self._upload_to_s3(_img_data)

    def upload_image(self, img_src, key=None):
        self.key = '' if key is None else key
        try:
            _img_data = Image.open(requests.get(img_src, stream=True).raw)
            return self._upload_to_s3(_img_data)

        except Exception as ex:
            return str(ex)[0:200], 300

    def _upload_to_s3(self, image_data):
        print(image_data.size)
        _img_body = self._get_body(image_data)
        if self.key == '':
            self.key = self._get_random_key(None, image_data.format)

        print("Uploading...")
        self.client.put_object(Body=_img_body, Key=self.key, Bucket=self.bucket_name, ContentType=self.type)
        print("Upload Done.")

        _img_s3_src = "https://{0}.s3.amazonaws.com/{1}".format(self.bucket_name, self.key)
        return _img_s3_src, 200

    def _get_body(self, image_data):
        self.width, self.height = image_data.size

        _img_bytes = io.BytesIO()
        image_data.save(_img_bytes, format=image_data.format)
        _img_body = _img_bytes.getvalue()
        return _img_body

    def _get_random_key(self, prefix=None, img_format=None):
        _prefix = prefix if prefix is not None else self.bucket_folder_name
        _img_format = 'jpg' if img_format is None or img_format == 'JPEG' else img_format.lower()

        _key = _prefix + datetime.now().strftime('%y-%m-%d-%H-%M-%S_%f.') + _img_format
        return _key
