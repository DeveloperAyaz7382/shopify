# app/crud.py
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from models import Media
from schemas import MediaCreate, ProductBase, ProductVariantCreate, ProductVariantUpdate
from schemas import UserCreate, UserUpdate, UserResponse
from models import User
from models import Product
from models import ProductVariant

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


# Create a new product
def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductBase) -> Product:
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product: ProductBase) -> Optional[Product]:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    return None

def delete_product(db: Session, product_id: int) -> bool:
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False



# # CRUD operations
# def get_product_variant(db: Session, variant_id: int):
#     return db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()

# def get_all_product_variants(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(ProductVariant).offset(skip).limit(limit).all()

# def create_product_variant(db: Session, variant: ProductVariantCreate):
#     db_variant = ProductVariant(**variant.dict())
#     db.add(db_variant)
#     db.commit()
#     db.refresh(db_variant)
#     return db_variant

# def update_product_variant(db: Session, variant_id: int, update_data: ProductVariantUpdate):
#     db_variant = get_product_variant(db, variant_id)
#     if not db_variant:
#         raise HTTPException(status_code=404, detail="ProductVariant not found")
#     for key, value in update_data.dict(exclude_unset=True).items():
#         setattr(db_variant, key, value)
#     db.commit()
#     db.refresh(db_variant)
#     return db_variant

# def delete_product_variant(db: Session, variant_id: int):
#     db_variant = get_product_variant(db, variant_id)
#     if not db_variant:
#         raise HTTPException(status_code=404, detail="ProductVariant not found")
#     db.delete(db_variant)
#     db.commit()
#     return {"detail": "ProductVariant deleted"}


# ✅ Create a new product variant
def create_product_variant(db: Session, variant_data: ProductVariantCreate):
    variant = ProductVariant(**variant_data.dict())
    db.add(variant)
    db.commit()
    db.refresh(variant)
    return variant

# ✅ Get all product variants
def get_product_variants(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ProductVariant).offset(skip).limit(limit).all()

# ✅ Get a single product variant by ID
def get_product_variant(db: Session, variant_id: int):
    return db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()

# ✅ Update a product variant
def update_product_variant(db: Session, variant_id: int, variant_data: ProductVariantUpdate):
    variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
    if variant:
        for key, value in variant_data.dict(exclude_unset=True).items():
            setattr(variant, key, value)
        db.commit()
        db.refresh(variant)
    return variant

# ✅ Delete a product variant
def delete_product_variant(db: Session, variant_id: int):
    variant = db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()
    if variant:
        db.delete(variant)
        db.commit()
    return variant