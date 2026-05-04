from datetime import date
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Photo, Anniversary, Trip, DiaryEntry
from app.dependencies import require_auth

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
async def home(request: Request, _=Depends(require_auth), db: Session = Depends(get_db)):
    days_together = (date.today() - settings.relationship_start_date).days
    recent_photos = db.query(Photo).order_by(Photo.created_at.desc()).limit(6).all()
    upcoming = db.query(Anniversary).order_by(Anniversary.date).limit(3).all()
    return templates.TemplateResponse("home.html", {
        "request": request,
        "days_together": days_together,
        "recent_photos": recent_photos,
        "anniversaries": upcoming,
        "site_title": settings.site_title,
        "relationship_start": settings.relationship_start_date.strftime("%Y-%m-%d"),
    })


@router.get("/gallery")
async def gallery(request: Request, _=Depends(require_auth), db: Session = Depends(get_db)):
    photos = db.query(Photo).order_by(Photo.taken_at.desc().nullslast()).all()

    all_tags = set()
    for p in photos:
        if p.tags:
            for t in p.tags:
                all_tags.add(t)

    return templates.TemplateResponse("gallery.html", {
        "request": request, "photos": photos, "all_tags": sorted(all_tags),
    })


@router.get("/timeline")
async def timeline(request: Request, _=Depends(require_auth), db: Session = Depends(get_db)):
    anniversaries = db.query(Anniversary).order_by(Anniversary.date).all()
    return templates.TemplateResponse("timeline.html", {
        "request": request, "anniversaries": anniversaries,
    })


@router.get("/map")
async def trip_map(request: Request, _=Depends(require_auth), db: Session = Depends(get_db)):
    trips = db.query(Trip).order_by(Trip.visited_at.desc()).all()
    return templates.TemplateResponse("map.html", {
        "request": request, "trips": trips,
    })


@router.get("/diary")
async def diary(request: Request, _=Depends(require_auth), db: Session = Depends(get_db)):
    entries = db.query(DiaryEntry).order_by(DiaryEntry.created_at.desc()).all()
    return templates.TemplateResponse("diary.html", {
        "request": request, "entries": entries,
    })


@router.get("/admin")
async def admin_page(request: Request, db: Session = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse("/login")
    photos = db.query(Photo).order_by(Photo.created_at.desc()).all()
    anniversaries = db.query(Anniversary).order_by(Anniversary.date).all()
    trips = db.query(Trip).order_by(Trip.visited_at.desc()).all()
    entries = db.query(DiaryEntry).order_by(DiaryEntry.created_at.desc()).all()
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "photos": photos,
        "anniversaries": anniversaries,
        "trips": trips,
        "entries": entries,
    })
