import json
import boto3
import time
import os

bucket_name = os.environ["BUCKET_NAME"]
s3 = boto3.resource("s3")
bucket = s3.Bucket(bucket_name)


def lambda_handler(event, context):
        
    obj = s3.Object(bucket_name, f"log-{time.time()}.txt")
    obj.put(Body=json.dumps(event))
    print(event)
    return {"event": event, "message": "object Inserted successfully."}
