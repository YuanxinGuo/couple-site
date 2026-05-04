from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models import Trip
from app.dependencies import require_admin

router = APIRouter()


@router.post("")
async def create_trip(
    place: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    visited_at: str = Form(...),
    story: str = Form(""),
    _=Depends(require_admin),
    db: Session = Depends(get_db),
):
    trip = Trip(
        place=place,
        latitude=latitude,
        longitude=longitude,
        visited_at=date.fromisoformat(visited_at),
        story=story,
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return {"ok": True, "id": trip.id}


@router.delete("/{trip_id}")
async def delete_trip(
    trip_id: int,
    _=Depends(require_admin),
    db: Session = Depends(get_db),
):
    trip = db.query(Trip).get(trip_id)
    if not trip:
        raise HTTPException(404)
    db.delete(trip)
    db.commit()
    return {"ok": True}
