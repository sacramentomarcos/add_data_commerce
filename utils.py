import boto3
from dotenv import load_dotenv
from os import environ
from pprint import pprint
from datetime import datetime
from typing import Literal
import re

load_dotenv()

def get_s3():
    session = boto3.Session(aws_access_key_id=environ['aws_access_key_id'],
                        aws_secret_access_key=environ['aws_secret_access_key'],
                        region_name=environ['aws_region'],
                        aws_account_id=environ['aws_account_id'])

    s3 = session.client("s3")
    return s3


def get_buckets(s3=None):
    return [bucket['Name'] for bucket in s3.list_buckets()['Buckets']]

def get_bucket_content(s3, bucket_name:str, mode:Literal['folder', 'archive']):
    paginator = s3.get_paginator('list_objects_v2')
    
    content = [i['Key'] for page in paginator.paginate(Bucket=bucket_name) for i in page['Contents']]

    if mode == 'folder':
        return list(filter(lambda x: x[-1] == '/' and re.search('[0-9]{2}_[0-9]{2}_[0-9]{4}', x), content))
    elif mode == 'archive':
        return list(filter(lambda x: x[-1] != '/' and re.search('[0-9]{2}_[0-9]{2}_[0-9]{4}', x), content))

def get_max_date(content:list[str]):
    dates = {
        datetime.strptime(k.split('ingestion_date=')[1][:-1], '%d_%m_%Y') # data após 
        for k in content
        if 'ingestion_date=' in k
        }
    return max(dates)