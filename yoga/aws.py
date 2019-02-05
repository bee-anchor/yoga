import boto3


def upload_screenshot_to_s3(filename, file, bucket_name, aws_access_key=None,
                            aws_secret_access_key=None, aws_session_token=None, region_name=None):
    if aws_access_key and aws_secret_access_key and aws_session_token:
        s3 = boto3.resource('s3', aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_access_key,
                            aws_session_token=aws_session_token, region_name=region_name)
    else:
        s3 = boto3.resource('s3')

    s3.Bucket(bucket_name).put_object(Key=filename, Body=file, ContentType='image/png', ACL='private')
    url = f'{s3.meta.client.meta.endpoint_url}/{bucket_name}/{filename}'
    print(url)
    return url

def get_s3_file_contents_as_string(bucket_name, filename, aws_access_key=None,
                                   aws_secret_access_key=None, aws_session_token=None, region_name=None):
    if aws_access_key and aws_secret_access_key and aws_session_token:
        s3 = boto3.resource('s3', aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_access_key,
                            aws_session_token=aws_session_token, region_name=region_name)
    else:
        s3 = boto3.resource('s3')

    obj = s3.Object(bucket_name, filename)
    return obj.get()['Body'].read().decode('utf-8')

def get_secure_ssm_parameter(name, aws_access_key=None, aws_secret_access_key=None,
                             aws_session_token=None, region_name=None):
    if aws_access_key and aws_secret_access_key and aws_session_token:
        ssm = boto3.client('ssm', aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_access_key,
                            aws_session_token=aws_session_token, region_name=region_name)
    else:
        ssm = boto3.client('ssm')
    return ssm.get_parameter(Name=name, WithDecryption=True)['Parameter']['Value']