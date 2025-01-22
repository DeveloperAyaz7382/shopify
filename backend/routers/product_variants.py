from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import ProductVariant
from schemas import ProductVariantCreate, ProductVariantUpdate, ProductVariantResponse

router = APIRouter(prefix="/product_variants", tags=["Product Variants"])

# CRUD Operations
def get_variant(db: Session, variant_id: int) -> ProductVariant:
    return db.query(ProductVariant).filter(ProductVariant.id == variant_id).first()

def get_variants(db: Session, skip: int = 0, limit: int = 10) -> list[ProductVariant]:
    return db.query(ProductVariant).offset(skip).limit(limit).all()

def create_variant(db: Session, variant: ProductVariantCreate) -> ProductVariant:
    db_variant = ProductVariant(**variant.dict())
    db.add(db_variant)
    db.commit()
    db.refresh(db_variant)
    return db_variant

def update_variant(db: Session, variant_id: int, variant: ProductVariantUpdate) -> ProductVariant:
    db_variant = get_variant(db, variant_id)
    if not db_variant:
        return None
    for key, value in variant.dict(exclude_unset=True).items():
        setattr(db_variant, key, value)
    db.commit()
    db.refresh(db_variant)
    return db_variant

def delete_variant(db: Session, variant_id: int) -> bool:
    db_variant = get_variant(db, variant_id)
    if not db_variant:
        return False
    db.delete(db_variant)
    db.commit()
    return True

# Routes
@router.get("/", response_model=List[ProductVariantResponse])
def read_variants(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_variants(db, skip=skip, limit=limit)

@router.get("/{variant_id}", response_model=ProductVariantResponse)
def read_variant(variant_id: int, db: Session = Depends(get_db)):
    variant = get_variant(db, variant_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Product Variant not found")
    return variant

@router.post("/", response_model=ProductVariantResponse)
def create_variant_endpoint(variant: ProductVariantCreate, db: Session = Depends(get_db)):
    return create_variant(db, variant)

@router.put("/{variant_id}", response_model=ProductVariantResponse)
def update_variant_endpoint(variant_id: int, variant: ProductVariantUpdate, db: Session = Depends(get_db)):
    updated_variant = update_variant(db, variant_id, variant)
    if not updated_variant:
        raise HTTPException(status_code=404, detail="Product Variant not found")
    return updated_variant

@router.delete("/{variant_id}", response_model=dict)
def delete_variant_endpoint(variant_id: int, db: Session = Depends(get_db)):
    success = delete_variant(db, variant_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product Variant not found")
    return {"message": "Product Variant deleted successfully"}
