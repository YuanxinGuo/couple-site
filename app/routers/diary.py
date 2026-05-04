from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import DiaryEntry
from app.dependencies import require_admin

router = APIRouter()


@router.post("")
async def create_entry(
    title: str = Form(""),
    content: str = Form(...),
    mood: str = Form("happy"),
    _=Depends(require_admin),
    db: Session = Depends(get_db),
):
    entry = DiaryEntry(
        title=title,
        content=content,
        mood=mood,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {"ok": True, "id": entry.id}


@router.delete("/{entry_id}")
async def delete_entry(
    entry_id: int,
    _=Depends(require_admin),
    db: Session = Depends(get_db),
):
    entry = db.query(DiaryEntry).get(entry_id)
    if not entry:
        raise HTTPException(404)
    db.delete(entry)
    db.commit()
    return {"ok": True}
