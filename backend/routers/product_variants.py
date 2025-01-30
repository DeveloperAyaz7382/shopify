from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
# from crud import create_product_variant, delete_product_variant, get_product_variant, update_product_variant
from database import get_db
from models import ProductVariant
from schemas import ProductVariantCreate, ProductVariantUpdate, ProductVariantResponse
import crud
router = APIRouter(prefix="/variants", tags=["Product Variants"])

class ProductVariant(BaseModel):
    product_id: int
    name: str
    sku: str = None
    price: float
    weight:float
    quantity: int
    compare_price:float




# ✅ Create a new product variant
@router.post("/", response_model=ProductVariantResponse)
def create_variant(variant_data: ProductVariantCreate, db: Session = Depends(get_db)):
    return crud.create_product_variant(db, variant_data)

# ✅ Get all product variants
@router.get("/", response_model=list[ProductVariantResponse])
def list_variants(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_product_variants(db, skip, limit)

# ✅ Get a single variant by ID
@router.get("/{variant_id}", response_model=ProductVariantResponse)
def get_variant(variant_id: int, db: Session = Depends(get_db)):
    variant = crud.get_product_variant(db, variant_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return variant

# ✅ Update a variant
@router.put("/{variant_id}", response_model=ProductVariantResponse)
def update_variant(variant_id: int, variant_data: ProductVariantUpdate, db: Session = Depends(get_db)):
    variant = crud.update_product_variant(db, variant_id, variant_data)
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return variant

# ✅ Delete a variant
@router.delete("/{variant_id}", response_model=ProductVariantResponse)
def delete_variant(variant_id: int, db: Session = Depends(get_db)):
    variant = crud.delete_product_variant(db, variant_id)
    if not variant:
        raise HTTPException(status_code=404, detail="Variant not found")
    return variant