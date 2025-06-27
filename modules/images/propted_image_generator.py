from  openai import OpenAI
import boto3
import uuid
import os
import base64
from dotenv import load_dotenv
load_dotenv()

class PromptedImageGenerator:
    def __init__(self):
        self.openai_client = OpenAI()
        self.s3_bucket_name = os.getenv("AWS_BUCKET_NAME")
        self.s3_folder = "cxplorers/generated-images"
        self.s3_client = boto3.client("s3")

    async def interact(self, user_id: str, input: str) -> str:
        try: 
            img = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=input,
                n=1,
                size="1024x1024",
                response_format="b64_json"
            )

            print(f"img response::::::")

            image_bytes = base64.b64decode(img.data[0].b64_json)

            filename = f"{user_id}/{uuid.uuid4()}.png"
            s3_key = f"{self.s3_folder}/{filename}"

            self.s3_client.put_object(
                Bucket=self.s3_bucket_name,
                Key=s3_key,
                Body=image_bytes,
                ContentType="image/png"
            )

            # Return the public S3 URL
            image_url = f"https://{self.s3_bucket_name}.s3.amazonaws.com/{s3_key}"
            print(image_url)
            return image_url

        except Exception as e :
            print(e)
        
       

        