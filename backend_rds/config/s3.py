import boto3
from botocore.exceptions import ClientError, NoCredentialsError, ConnectTimeoutError
import os 
from dotenv import load_dotenv

load_dotenv()

# client = boto3.client('s3')
bucket_name = os.getenv('S3_BUCKET_NAME')

#! Teste S3 on local host
session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN'),
)

teste_client = session.client('s3')

conditions = [
    {"key": "Content-Type", "eq": "application/x-parquet"},
    {"key": "Content-Length", "lte": 50 * 1024 * 1024}
]

def generate_presigned_post(bucket_name,
                            expiration=3600, 
                            object_name='',
                            fields=None,
                            conditions=conditions
                        ):
    try:
        response = teste_client.generate_presigned_post(bucket_name,
                                                    object_name,
                                                    Fields=fields,
                                                    Conditions=conditions,
                                                    ExpiresIn=expiration)
    except (ClientError, NoCredentialsError, ConnectTimeoutError) as e:
        raise e
    return response
