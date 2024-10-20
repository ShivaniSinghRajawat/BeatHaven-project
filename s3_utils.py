import boto3
from botocore.exceptions import ClientError
from config import Config

s3_client = boto3.client('s3',
                         aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                         region_name=Config.AWS_REGION)

def upload_file_to_s3(file, object_name=None):
    if object_name is None:
        object_name = file.filename

    try:
        s3_client.upload_fileobj(file, Config.S3_BUCKET, object_name)
    except ClientError as e:
        print(e)
        return False
    return True

def get_s3_url(object_name):
    try:
        url = s3_client.generate_presigned_url('get_object',
                                               Params={'Bucket': Config.S3_BUCKET,
                                                       'Key': object_name},
                                               ExpiresIn=3600)
    except ClientError as e:
        print(e)
        return None
    return url