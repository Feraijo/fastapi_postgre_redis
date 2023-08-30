import datetime
from typing import Optional

from pydantic import BaseModel


class DocumentType(BaseModel):
    typename: str
    extension: str

# Shared properties
class DocumentBase(BaseModel):
    docname: str
    doc_type: DocumentType
    date_update: Optional[datetime.datetime]
    #bin_contents: bytes


# Properties to receive on item creation
class DocumentCreate(DocumentBase):
    date_create: datetime.datetime


# Properties to receive on item update
class DocumentUpdate(DocumentBase):
    date_update: datetime.datetime


# Properties shared by models stored in DB
class DocumentInDBBase(DocumentCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class Document(DocumentInDBBase):
    pass


# Properties properties stored in DB
class DocumentInDB(DocumentInDBBase):
    pass
