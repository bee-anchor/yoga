import boto
from boto.s3.key import Key
from faf.context import CONTEXT


def upload_screenshot_to_s3(filename, file):
    bucket_name = CONTEXT.config['remote_grid']['remote_screenshot_s3_bucket']
    if CONTEXT.config.has_option('remote_grid', 's3_access_key') and CONTEXT.config.has_option('remote_grid', 's3_secret_access_key'):
        conn = boto.connect_s3(CONTEXT.config['remote_grid']['s3_access_key'], CONTEXT.config['remote_grid']['s3_secret_access_key'])
    else:
        conn = boto.connect_s3()
    bucket = conn.get_bucket(bucket_name)
    k = Key(bucket)
    k.key = filename
    k.set_contents_from_string(file)
    url = k.generate_url(expires_in=0, query_auth=False)
    print(url)
    return url
