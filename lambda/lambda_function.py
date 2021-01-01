import logging
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)
logging.basicConfig(level=logging.INFO)

import boto3
import tempfile
import json
import config
import tweets as t


def __get_temporary_file_from_s3(bucket, object_name) -> tempfile.NamedTemporaryFile:
        object = bucket.Object(object_name)
        tmp = tempfile.NamedTemporaryFile()

        with open(tmp.name, 'wb') as f:
            object.download_fileobj(f)

        return tmp


def lambda_handler(event, context):
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(config.BUCKET_NAME)

    data_file = __get_temporary_file_from_s3(bucket, config.S3_PATH)

    data = None
    with open(data_file.name, 'r') as f:
        data = json.load(f)

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
