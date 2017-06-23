from src.service.aws.s3 import AwsS3

img_url = 'https://static01.nyt.com/images/2017/06/06/business/06TRUMPHOTEL2/06TRUMPHOTEL2-facebookJumbo.jpg'
img_url2 = 'https://cdn2.tnwcdn.com/wp-content/blogs.dir/1/files/2017/06/Screen-Shot-2017-06-06-at-12.53.40.png'
img_local_path = 'www/asset/img/demo-r2.png'
img_key = 'asset/img/demo-r2_thumb.png'

BUCKET_NAME = '3w-static'
s3 = AwsS3()
# s3_src, status = s3.upload_local_image(img_local_path)
# print(s3_src)

s3_src, status = s3.upload_image(img_url)
print(s3_src)
