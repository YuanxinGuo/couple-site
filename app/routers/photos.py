from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import Photo
from app.dependencies import require_admin
from app.services.cloudinary_service import upload_image, delete_image

router = APIRouter()


@router.post("/upload")
async def upload_photo(
    file: UploadFile = File(...),
    caption: str = Form(""),
    location: str = Form(""),
    taken_at: str = Form(""),
    tags: str = Form(""),
    _=Depends(require_admin),
    db: Session = Depends(get_db),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "仅支持图片格式")

    contents = await file.read()
    result = upload_image(contents, folder="couple")

    photo = Photo(
        public_id=result["public_id"],
        url=result["url"],
        thumb_url=result["thumb_url"],
        caption=caption,
        location=location,
        taken_at=datetime.fromisoformat(taken_at) if taken_at else None,
        tags=[t.strip() for t in tags.split(",") if t.strip()],
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return {"id": photo.id, "url": photo.url}


@router.delete("/{photo_id}")
async def delete_photo(
    photo_id: int,
    _=Depends(require_admin),
    db: Session = Depends(get_db),
):
    photo = db.query(Photo).get(photo_id)
    if not photo:
        raise HTTPException(404)
    delete_image(photo.public_id)
    db.delete(photo)
    db.commit()
    return {"ok": True}
