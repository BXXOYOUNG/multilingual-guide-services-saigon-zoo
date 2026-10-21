"""Read-only check of SeaweedFS S3 API configuration; prints no credentials."""
import os

import boto3


client = boto3.client(
    "s3",
    endpoint_url=os.environ.get("AUDIO_STORAGE_ENDPOINT_URL"),
    region_name=os.environ.get("AUDIO_STORAGE_REGION", "us-east-1"),
    aws_access_key_id=os.environ.get("AUDIO_STORAGE_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AUDIO_STORAGE_SECRET_ACCESS_KEY"),
)
bucket = os.environ.get("AUDIO_STORAGE_BUCKET", "")
buckets = {item["Name"] for item in client.list_buckets().get("Buckets", [])}
print("s3_api_reachable=True")
print(f"configured_bucket_exists={bucket in buckets}")
print(f"bucket_count={len(buckets)}")
