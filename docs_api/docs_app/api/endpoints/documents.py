from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from docs_app.controllers.document import document_controller
from docs_app.schemas import DocumentSchema, DocumentCreate, DocumentUpdate
from docs_app.core.dependencies import get_db, get_current_user
from docs_app.db.models.db_models import User

router = APIRouter()


@router.get("/", response_model=List[DocumentSchema])
async def get_documents(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Получить документы пользователя.
    """
    items = await document_controller.get_multi_by_owner(
        db=db, user_id=current_user.id, skip=skip, limit=limit
    )
    return items


@router.post("/", response_model=DocumentCreate)
async def upload_document(
    file_in: UploadFile,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Загрузить документ в БД.
    """
    document = await document_controller.create_with_owner(
        db=db, file_in=file_in, user_id=current_user.id)
    return document


@router.put("/{id}", response_model=DocumentUpdate)
async def update_document(
    id: int,
    file_in: UploadFile,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Обновить документ по id.
    """
    document = await document_controller.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    document = await document_controller.update_document(db=db, db_obj=document, file_in=file_in)
    return document


@router.get("/{id}", response_model=DocumentSchema)
async def get_document(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Получить документ по id.
    """
    document = await document_controller.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/download/{id}")
async def download_document(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Скачать документ по id.
    """
    document = await document_controller.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    with open("contents", "wb") as binary_file:
        binary_file.write(document.bin_contents)
        return FileResponse("contents",
            filename=document.docname,
            media_type='multipart/form-data',
        )


@router.delete("/{id}", response_model=DocumentSchema)
async def delete_document(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Удалить документ по id.
    """
    document = await document_controller.get(db=db, id=id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    document = await document_controller.remove(db=db, id=id)
    return document
