from pydantic import BaseModel


class Document(BaseModel):
    temperature: int
    humidity: int
    overcast: str
    wind_speed: int


class User(BaseModel):
    full_name: str
    login: str
    document: Document
