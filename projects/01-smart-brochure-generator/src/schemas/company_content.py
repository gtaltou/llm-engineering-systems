from pydantic import BaseModel


class CompanyContent(BaseModel):
    url: str
    title: str
    content: str
