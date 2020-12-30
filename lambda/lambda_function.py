import boto3
import tempfile
import json
import tweets as t
import logging


def lambda_handler(event, context):
    logging.basicConfig()
    try:

        bucket_name = "latest-research-pl"
        s3_path = 'data.json'

        s3 = boto3.resource("s3")
        bucket = s3.Bucket(bucket_name)
        object = bucket.Object('data.json')
        tmp = tempfile.NamedTemporaryFile()

        data = None
        with open(tmp.name, 'wb') as f:
            object.download_fileobj(f)

        with open(tmp.name, 'r') as f:
            data = json.load(f)

        new_data = t.get_updated_tweets(data)
        new_data_str = json.dumps(new_data)
        encoded_string = new_data_str.encode("utf-8")

        bucket.put_object(Key=s3_path, Body=encoded_string)

        return {
            'statusCode': 200
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'exception': e
        }
