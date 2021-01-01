import logging
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
logging.basicConfig(level=logging.INFO)

import boto3
import tempfile
import json
import config
import tweets as t
from botocore.errorfactory import ClientError


def __get_data(bucket, object_name) -> dict:
    s3obj = bucket.Object(object_name)
    try:
        s3obj.load()
    except ClientError:
        return {} # there is no data.json file yet

    tmp = tempfile.NamedTemporaryFile()
    with open(tmp.name, 'wb') as f:
        s3obj.download_fileobj(f)

    with open(tmp.name, 'r') as f:
        data = json.load(f)
        return data


def lambda_handler(event, context):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(config.BUCKET_NAME)

    data = __get_data(bucket, config.S3_PATH)

    since_id = data.get('since_id')
    existing_tweets = data.get('tweets') or []

    since_id, tweets = t.get_updated_tweets(since_id, existing_tweets)
    result = {
        'since_id': since_id,
        'tweets': tweets
    }

    new_data_str = json.dumps(result)
    encoded_string = new_data_str.encode("utf-8")

    bucket.put_object(Key=config.S3_PATH, Body=encoded_string)

    return {
        'statusCode': 200
    }
