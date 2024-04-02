from pydantic import BaseModel


class DocumentResponse(BaseModel):
    page_content: str
    metadata: dict
