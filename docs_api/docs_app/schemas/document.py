import datetime
from typing import Optional

from pydantic import BaseModel


class DocumentType(BaseModel):
    typename: str
    extension: str


class DocumentBase(BaseModel):
    docname: str
    doc_type: DocumentType
    date_update: Optional[datetime.datetime]


class DocumentCreate(DocumentBase):
    date_create: datetime.datetime


class DocumentUpdate(DocumentBase):
    date_update: datetime.datetime


class DocumentInDBBase(DocumentCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class DocumentSchema(DocumentInDBBase):
    pass
