from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Float, Boolean, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)
    public_id = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    thumb_url = Column(String(500), nullable=False)
    caption = Column(Text, default="")
    taken_at = Column(DateTime, nullable=True)
    location = Column(String(200), default="")
    tags = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class Anniversary(Base):
    __tablename__ = "anniversaries"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text, default="")
    icon = Column(String(50), default="❤️")
    recurring = Column(Boolean, default=True)


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    place = Column(String(200), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    visited_at = Column(Date, nullable=False)
    story = Column(Text, default="")
    photo_ids = Column(JSON, default=list)


class DiaryEntry(Base):
    __tablename__ = "diary_entries"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), default="")
    content = Column(Text, nullable=False)
    mood = Column(String(50), default="happy")
    created_at = Column(DateTime, default=datetime.utcnow)
