import boto3
import requests
import io
from PIL import Image

ACCESS_KEY_ID = 'AKIAJQCZ2HHQ46Q2IAZA'
ACCESS_SECRET_KEY = ''


class AwsS3(object):
    type = 'image/jpeg'
    client = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=ACCESS_SECRET_KEY)
    bucket_name = '3w-static'
    key = ''
    width, height = 0, 0

    def __init__(self, bucket_name=None):
        if bucket_name is not None:
            self.bucket_name = bucket_name

    def upload_local_image(self, img_path, key=None):
        self.key = key

        _img_data = Image.open(img_path)
        self._upload_to_s3(_img_data)

    def upload_image(self, img_src, key=None):
        self.key = key

        _img_data = Image.open(requests.get(img_src, stream=True).raw)
        self._upload_to_s3(_img_data)

    def _upload_to_s3(self, image_data):
        print(image_data.size)
        _img_body = self._get_body(image_data)

        print("Uploading...")
        self.client.put_object(Body=_img_body, Key=self.key, Bucket=self.bucket_name, ContentType=self.type)
        print("Upload Done.")

    def _get_body(self, image_data):
        self.width, self.height = image_data.size

        _img_bytes = io.BytesIO()
        image_data.save(_img_bytes, format=image_data.format)
        _img_body = _img_bytes.getvalue()
        return _img_body
