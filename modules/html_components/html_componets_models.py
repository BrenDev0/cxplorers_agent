from pydantic import BaseModel

class HtmlRequest(BaseModel):
    connection_id: str;
    input: str
