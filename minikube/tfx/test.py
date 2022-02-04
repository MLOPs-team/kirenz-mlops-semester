from fileinput import filename
import logging
import boto3
from botocore.exceptions import ClientError
import os

AWS_ACCESS_KEY="AKIA25EGWZIMNUVOQNJQ"
AWS_SECERT_KEY="psvL/+lr35xT3PtkRckbTXcS7iGN24MQ/j0Iv4wQ"

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECERT_KEY)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def download_file(file_name, bucket, object_name):
    s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECERT_KEY)

    try:
        response = s3_client.download_file(file_name, bucket, object_name)
        print(response)
    except ClientError as e:
        logging.error(e)
        return False
    return True

filename = '/home/ec2-user/Development/MLOPS/kirenz-mlops-semester/minikube/tfx'
bucket = 'delta-lake-mlops'
object_name = 'part-00000-14f7d0fa-4962-451d-ac31-55402dbe2db0.c000.snappy.parquet'

download_file(filename, bucket,object_name)

#filename = "/home/ec2-user/Development/MLOPS/kirenz-mlops-semester/minikube/tfx/dataPreprocessing/pandas/GetData.ipynb"
#bucket = 'airflow-mlops'
#upload_file(filename, bucket)

