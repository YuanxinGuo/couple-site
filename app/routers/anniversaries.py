from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models import Anniversary
from app.dependencies import require_admin

router = APIRouter()


@router.post("")
async def create_anniversary(
    title: str = Form(...),
    date_str: str = Form(...),
    description: str = Form(""),
    icon: str = Form("❤️"),
    recurring: bool = Form(True),
    _=Depends(require_admin),
    db: Session = Depends(get_db),
):
    anniv = Anniversary(
        title=title,
        date=date.fromisoformat(date_str),
        description=description,
        icon=icon,
        recurring=recurring,
    )
    db.add(anniv)
    db.commit()
    db.refresh(anniv)
    return {"ok": True, "id": anniv.id}


@router.delete("/{anniv_id}")
async def delete_anniversary(
    anniv_id: int,
    _=Depends(require_admin),
    db: Session = Depends(get_db),
):
    anniv = db.query(Anniversary).get(anniv_id)
    if not anniv:
        raise HTTPException(404)
    db.delete(anniv)
    db.commit()
    return {"ok": True}
