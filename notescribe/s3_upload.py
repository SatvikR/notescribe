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

def upload_file(file_path: str, s3_path: str, make_public=False) -> bool:
    '''
    Uploads a file to an S3 bucket
    
    :param file_path: Path to file to upload
    :param s3_path: S3 object name to upload to (e.g. myfolder/myfile)
    :param make_public: If True, then the uploaded file will be made public
    :return: True if the file was uploaded, otherwise False
    '''

    try:
        if make_public:
            s3_client.upload_file(file_path, s3_bucket_name, s3_path, ExtraArgs={'ACL': 'public-read'})
        else:
            s3_client.upload_file(file_path, s3_bucket_name, s3_path)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def get_url(s3_path: str) -> str:
    '''
    Gets the web url of the specified s3 object
    
    :param s3_path: S3 object name to get url of (e.g. myfolder/myfile)
    :return: The url ofthe provided object
    '''
    return f"https://{s3_bucket_name}.s3.amazonaws.com/{s3_path}"
