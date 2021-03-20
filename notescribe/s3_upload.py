from notescribe import settings
import logging
import boto3
from botocore.exceptions import ClientError

s3_bucket_name = settings['s3_bucket']
_aws_auth_key = settings.get('aws_access_key')
_aws_secret_key = settings.get('aws_secret_key')

s3_client = None
if not _aws_auth_key == None and not _aws_secret_key == None:
    s3_client = boto3.client('s3',
        aws_access_key_id=_aws_auth_key,
        aws_secret_access_key=_aws_secret_key
    )
else:
    s3_client = boto3.client('s3')
del _aws_auth_key, _aws_secret_key

def upload_file(file_path: str, s3_path: str) -> bool:
    '''
    Uploads a file to an S3 bucket
    
    :param file_path: Path to file to upload
    :param s3_path: S3 object name to upload to (e.g. myfolder/myfile)
    :return: True if the file was uploaded, otherwise False
    '''

    try:
        response = s3_client.upload_file(file_path, s3_bucket_name, s3_path)
    except ClientError as e:
        logging.error(e)
        return False
    return True
