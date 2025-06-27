from pydantic import BaseModel

class HtmlRequest(BaseModel):
    input: str
