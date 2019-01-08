import boto
from boto.s3.key import Key


def upload_screenshot_to_s3(filename, file, bucket_name, s3_access_key=None, s3_secret_access_key=None):
    if s3_access_key and s3_secret_access_key:
        conn = boto.connect_s3(s3_access_key, s3_secret_access_key)
    else:
        conn = boto.connect_s3()
    bucket = conn.get_bucket(bucket_name)
    k = Key(bucket)
    k.key = filename
    k.set_contents_from_string(file)
    url = k.generate_url(expires_in=0, query_auth=False)
    print(url)
    return url
