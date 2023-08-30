import datetime
from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from docs_app.db.models.db_models import Document, DocumentType
from sqlalchemy import select


class DocumentController():
    @staticmethod
    def get_file_extension(filename):
        return filename.rsplit('.', 1)[-1]

    async def _get_doc_type(self, db: AsyncSession, typename: str, extension: str) -> DocumentType:
        result = await db.scalars(select(DocumentType).where(
                DocumentType.typename==typename,
                DocumentType.extension==extension,
            ))
        doc_type_obj = result.first()
        if not doc_type_obj:
            doc_type_obj = DocumentType(typename=typename,
                extension=extension)
            db.add(doc_type_obj)
        return doc_type_obj

    async def get(self, db: AsyncSession, id: int) -> Document:
        result = await db.scalars(
            select(Document)
            .filter(Document.id == id)
            .options(selectinload(Document.doc_type))
        )
        return result.first()

    async def create_with_owner(
        self, db: AsyncSession, file_in: UploadFile, user_id: int
    ) -> Document:
        doc_type_obj = await self._get_doc_type(
            db,
            file_in.content_type,
            self.get_file_extension(file_in.filename)
        )
        db_obj = Document(
            docname=file_in.filename,
            user_id=user_id,
            doc_type=doc_type_obj,
            date_create=datetime.datetime.now(),
            bin_contents=await file_in.read(),
        )
        await file_in.close()
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj, ['doc_type'])
        return db_obj

    async def get_multi_by_owner(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Document]:
        lst = await db.scalars(
            select(Document)
            .where(Document.user_id==user_id)
            .options(selectinload(Document.doc_type))
            .offset(skip)
            .limit(limit))
        return lst.all()
    
    async def update_document(
        self, db: AsyncSession, file_in: UploadFile, db_obj: Document,
    ) -> Document:
        doc_type_obj = await self._get_doc_type(
            db,
            file_in.content_type,
            self.get_file_extension(file_in.filename)
        )
        db_obj.docname = file_in.filename
        db_obj.date_update = datetime.datetime.now()
        db_obj.doc_type = doc_type_obj
        db_obj.bin_contents = await file_in.read()
        
        await file_in.close()
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj, ['doc_type'])
        return db_obj
    
    async def remove(self, db: Session, id: int) -> Document:
        obj = await self.get(db, id)
        await db.delete(obj)
        await db.commit()
        return obj


document_controller = DocumentController()
