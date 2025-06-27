from pydantic import BaseModel

class ImageGenerationREquest(BaseModel):
    input: str