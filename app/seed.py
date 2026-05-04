from datetime import date
from sqlalchemy.orm import Session
from app.models import Anniversary, Trip
from app.database import SessionLocal


def seed(db: Session, relationship_start: date):
    # 纪念日
    existing_anniv = db.query(Anniversary).count()
    if existing_anniv == 0:
        anniversaries = [
            Anniversary(
                title="在一起",
                date=relationship_start,
                description="我们在一起的第一天",
                icon="💕",
                recurring=True,
            ),
        ]
        db.add_all(anniversaries)
        print(f"Seeded {len(anniversaries)} anniversaries")

    # 足迹
    existing_trips = db.query(Trip).count()
    if existing_trips == 0:
        trips = [
            Trip(
                place="武汉",
                latitude=30.5928,
                longitude=114.3055,
                visited_at=date(2026, 4, 3),
                story="",
            ),
            Trip(
                place="北京",
                latitude=39.9042,
                longitude=116.4074,
                visited_at=date(2026, 4, 13),
                story="",
            ),
        ]
        db.add_all(trips)
        print(f"Seeded {len(trips)} trips")

    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        from app.config import settings
        seed(db, settings.relationship_start_date)
    finally:
        db.close()
