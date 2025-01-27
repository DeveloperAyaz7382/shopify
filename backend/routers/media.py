# # app/routers/media.py
# from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
# from sqlalchemy.orm import Session
# from models import Media
# from database import get_db
# import os
# import shutil
# from pathlib import Path
# # app/crud.py
# from schemas import MediaCreate



# router = APIRouter()



# def create_media(db: Session, media: MediaCreate):
#     db_media = Media(
#         filename=media.filename,
#         file_url=media.file_url,
#         file_size=media.file_size,
#         file_type=media.file_type
#     )
#     db.add(db_media)
#     db.commit()
#     db.refresh(db_media)
#     return db_media

# def get_media(db: Session, media_id: int):
#     return db.query(Media).filter(Media.id == media_id).first()

# def get_all_media(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(Media).offset(skip).limit(limit).all()


# # Directory to save uploaded images
# UPLOAD_DIRECTORY = "uploads"
# Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

# # Helper function to save file
# def save_file(file: UploadFile, upload_dir: str):
#     file_location = os.path.join(upload_dir, file.filename)
#     with open(file_location, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     return file_location

# @router.post("/upload/")
# async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     # Save the uploaded file to the directory
#     file_location = save_file(file, UPLOAD_DIRECTORY)
    
#     # Gather file metadata
#     file_size = os.path.getsize(file_location)
#     file_type = file.content_type
    
#     # Create a Media object
#     media_data = MediaCreate(
#         filename=file.filename,
#         file_url=file_location,
#         file_size=file_size,
#         file_type=file_type
#     )
    
#     # Store media in database
#     db_media = create_media(db=db, media=media_data)
#     return {"filename": db_media.filename, "file_url": db_media.file_url}

# @router.get("/media/{media_id}")
# def get_media(media_id: int, db: Session = Depends(get_db)):
#     media = get_media(db, media_id=media_id)
#     if media is None:
#         raise HTTPException(status_code=404, detail="Media not found")
#     return {"filename": media.filename, "file_url": media.file_url, "file_size": media.file_size, "file_type": media.file_type, "created_at": media.created_at}

# @router.get("/media/")
# def get_all_media(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     media = get_all_media(db, skip=skip, limit=limit)
#     return media

# app/routers/media.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Media
from database import get_db
import os
import shutil
from pathlib import Path
from schemas import MediaCreate
from crud import create_media as crud_create_media, get_media as crud_get_media, get_all_media as crud_get_all_media  # Import CRUD operations

router = APIRouter()

# Directory to save uploaded images
UPLOAD_DIRECTORY = "uploads"
Path(UPLOAD_DIRECTORY).mkdir(parents=True, exist_ok=True)

# Helper function to save file
def save_file(file: UploadFile, upload_dir: str):
    file_location = os.path.join(upload_dir, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return file_location

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Save the uploaded file to the directory
    file_location = save_file(file, UPLOAD_DIRECTORY)
    
    # Gather file metadata
    file_size = os.path.getsize(file_location)
    file_type = file.content_type
    
    # Create a MediaCreate object
    media_data = MediaCreate(
        filename=file.filename,
        file_url=file_location,
        file_size=file_size,
        file_type=file_type
    )
    
    # Store media in the database
    db_media = crud_create_media(db=db, media=media_data)
    return {"filename": db_media.filename, "file_url": db_media.file_url}

@router.get("/media/{media_id}")
def get_single_media(media_id: int, db: Session = Depends(get_db)):  # Renamed local function to avoid conflict
    media = crud_get_media(db, media_id=media_id)
    if media is None:
        raise HTTPException(status_code=404, detail="Media not found")
    return {"filename": media.filename, "file_url": media.file_url, "file_size": media.file_size, "file_type": media.file_type, "created_at": media.created_at}

@router.get("/media/")
def get_all_media(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):  # Renamed local function to avoid conflict
    media = crud_get_all_media(db, skip=skip, limit=limit)
    return media
