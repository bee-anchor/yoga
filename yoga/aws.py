import boto3


def upload_screenshot_to_s3(filename, file, bucket_name, s3_access_key=None, s3_secret_access_key=None):
    if s3_access_key and s3_secret_access_key:
        s3 = boto3.resource('s3', aws_access_key_id=s3_access_key, aws_secret_access_key=s3_secret_access_key)
    else:
        s3 = boto3.resource('s3')

    s3.Bucket(bucket_name).put_object(Key=filename, Body=file, ContentType='image/png', ACL='private')
    url = f'{s3.meta.client.meta.endpoint_url}/{bucket_name}/{filename}'
    print(url)
    return url
