import boto3
import os
from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
)


async def upload_to_s3(file_path: str, prefix: str) -> str:
    bucket = os.getenv("S3_BUCKET_NAME")
    object_name = f"{prefix}{os.path.basename(file_path)}"
    try:
        s3_client.upload_file(file_path, bucket, object_name)
        file_url = f"https://{bucket}.s3.amazonaws.com/{object_name}"
        return file_url
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="File not found for upload")
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
