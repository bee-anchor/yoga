import boto3


def upload_screenshot_to_s3(filename, file, bucket_name, aws_access_key=None,
                            aws_secret_access_key=None, aws_session_token=None, region_name=None):
    s3 = boto3.resource('s3', aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_access_key,
                            aws_session_token=aws_session_token, region_name=region_name)

    s3.Bucket(bucket_name).put_object(Key=filename, Body=file, ContentType='image/png', ACL='private')
    url = f'https://{bucket_name}.s3.amazonaws.com/{filename}'
    print(url)
    return url

def get_s3_file_contents_as_string(bucket_name, filename, aws_access_key=None,
                                   aws_secret_access_key=None, aws_session_token=None, region_name=None):
    s3 = boto3.resource('s3', aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_access_key,
                            aws_session_token=aws_session_token, region_name=region_name)

    obj = s3.Object(bucket_name, filename)
    return obj.get()['Body'].read().decode('utf-8')

def get_secure_ssm_parameter(name, aws_access_key=None, aws_secret_access_key=None,
                             aws_session_token=None, region_name=None):
    ssm = boto3.client('ssm', aws_access_key_id=aws_access_key,
                            aws_secret_access_key=aws_secret_access_key,
                            aws_session_token=aws_session_token, region_name=region_name)
    return ssm.get_parameter(Name=name, WithDecryption=True)['Parameter']['Value']