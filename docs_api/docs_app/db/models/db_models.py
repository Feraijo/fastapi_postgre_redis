import datetime
from typing import List
from sqlalchemy import String, ForeignKey, UniqueConstraint

from docs_app.db.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    full_name: Mapped[str] = mapped_column(String(50))
    hashed_password: Mapped[str] = mapped_column(String)
    documents: Mapped[List["Document"]] = relationship(cascade="all, delete-orphan")


class DocumentType(Base):
    __tablename__ = "doc_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    typename: Mapped[str] = mapped_column(String(200))
    extension: Mapped[str] = mapped_column(String(30))
    UniqueConstraint(typename, extension)


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    docname: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    type_id: Mapped[int] = mapped_column(ForeignKey(DocumentType.id))
    date_create: Mapped[datetime.datetime] = mapped_column(nullable=True)
    date_update: Mapped[datetime.datetime] = mapped_column(nullable=True)
    bin_contents: Mapped[bytes]

    doc_type: Mapped[DocumentType] = relationship()
