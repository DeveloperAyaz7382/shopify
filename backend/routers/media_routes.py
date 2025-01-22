from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4
from schemas import MediaCreate, MediaUpdate, MediaResponse
from database import get_db
from models import Media

# **CRUD Operations**

# Get a media item by ID
def get_media(db: Session, media_id: int):
    return db.query(Media).filter(Media.id == media_id).first()

# Get a list of media items with pagination
def get_media_list(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Media).offset(skip).limit(limit).all()

# Create a new media item
def create_media(db: Session, media_data: dict):
    media_data['uuid'] = uuid4()  # generate a new UUID for the media
    db_media = Media(**media_data)
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media

# Update an existing media item
def update_media(db: Session, media_id: int, media_data: dict):
    db_media = get_media(db, media_id)
    if db_media:
        for key, value in media_data.items():
            setattr(db_media, key, value)
        db.commit()
        db.refresh(db_media)
        return db_media
    return None

# Delete a media item
def delete_media(db: Session, media_id: int):
    db_media = get_media(db, media_id)
    if db_media:
        db.delete(db_media)
        db.commit()
        return True
    return False

# **FastAPI Routes**

router = APIRouter(prefix="/media", tags=["Media"])

# Get a list of media items
@router.get("/", response_model=List[MediaResponse])
def read_media(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_media_list(db, skip=skip, limit=limit)

# Get a single media item by ID
@router.get("/{media_id}", response_model=MediaResponse)
def read_single_media(media_id: int, db: Session = Depends(get_db)):
    media = get_media(db, media_id)
    if media is None:
        raise HTTPException(status_code=404, detail="Media not found")
    return media

# Create a new media item
@router.post("/", response_model=MediaResponse)
def create_new_media(media: MediaCreate, db: Session = Depends(get_db)):
    media_data = media.dict()
    return create_media(db, media_data)

# Update an existing media item
@router.put("/{media_id}", response_model=MediaResponse)
def update_existing_media(media_id: int, media: MediaUpdate, db: Session = Depends(get_db)):
    media_data = media.dict(exclude_unset=True)
    updated_media = update_media(db, media_id, media_data)
    if not updated_media:
        raise HTTPException(status_code=404, detail="Media not found")
    return updated_media

# Delete a media item
@router.delete("/{media_id}", response_model=dict)
def delete_existing_media(media_id: int, db: Session = Depends(get_db)):
    success = delete_media(db, media_id)
    if not success:
        raise HTTPException(status_code=404, detail="Media not found")
    return {"message": "Media deleted successfully"}
