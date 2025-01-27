# app/crud.py
from typing import List
from sqlalchemy.orm import Session
from models import Media
from schemas import MediaCreate
from schemas import UserCreate, UserUpdate, UserResponse
from models import User


# CRUD  Users)
def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate) -> User:
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True



# CRUD Media)

def create_media(db: Session, media: MediaCreate):
    db_media = Media(
        filename=media.filename,
        file_url=media.file_url,
        file_size=media.file_size,
        file_type=media.file_type
    )
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    return db_media

def get_media(db: Session, media_id: int):
    return db.query(Media).filter(Media.id == media_id).first()

def get_all_media(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Media).offset(skip).limit(limit).all()
