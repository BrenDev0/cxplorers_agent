from pydantic import BaseModel

class GenerateHtmlRequest(BaseModel):
    input: str