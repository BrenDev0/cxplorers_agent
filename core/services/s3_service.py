import boto3
from openai import OpenAI
import os
import uuid


class S3Service:
    def __init__(self):
        self.openai_client = OpenAI()
        self.s3_bucket_name = os.getenv("AWS_BUCKET_NAME")
        self.s3_client = boto3.client("s3")


    def upload(self, user_id: str, foldername: str, file_content: str | bytes, content_type: str) -> str:
        ext = "js" if "javascript" in content_type.lower() else "bin"
        filename = f"{user_id}/{uuid.uuid4()}.{ext}"
        s3_key = f"{foldername}/{filename}"

        if isinstance(file_content, str):
            file_content = file_content.encode('utf-8')

        self.s3_client.put_object(
            Bucket=self.s3_bucket_name,
            Key=s3_key,
            Body=file_content,
            ContentType=content_type
        )

        url = f"https://{self.s3_bucket_name}.s3.amazonaws.com/{s3_key}"
        print(url)
        return url