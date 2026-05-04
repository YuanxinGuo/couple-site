import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db, SessionLocal
from app.routers import pages, photos, anniversaries, trips, diary, auth
from app.seed import seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs("data", exist_ok=True)
    init_db()
    db = SessionLocal()
    try:
        seed(db, settings.relationship_start_date)
    finally:
        db.close()
    yield


app = FastAPI(title=settings.site_title, lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(auth.router)
app.include_router(pages.router)
app.include_router(photos.router, prefix="/api/photos", tags=["photos"])
app.include_router(anniversaries.router, prefix="/api/anniversaries", tags=["anniversaries"])
app.include_router(trips.router, prefix="/api/trips", tags=["trips"])
app.include_router(diary.router, prefix="/api/diary", tags=["diary"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
