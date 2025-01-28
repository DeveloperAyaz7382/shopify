# In router.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import schemas
from crud import get_product, get_products, create_product, update_product, delete_product
from models import Product
from database import SessionLocal  # Same with database module
from pydantic import BaseModel

from schemas import ProductUpdate  # Assuming this is a Pydantic schema for updating products
from models import Product  # Assuming Product is your ORM model
from schemas import ProductCreate  # Assuming ProductCreate is your Pydantic schema
from database import get_db  # Dependency for getting the database session
from crud import create_product  # Your function to handle product creation
from crud import update_product  # Your CRUD function for updating a product

router = APIRouter()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        

# Define the Pydantic model
class Product(BaseModel):
    id: int
    name: str
    price: float
    

    # Configuration for Pydantic v2
    model_config = {
        "from_attributes": True  # Enables ORM mode compatibility in Pydantic v2
    }

# Simulated data
sample_products = [
    {"id": 1, "name": "Product A", "price": 10.99},
    {"id": 2, "name": "Product B", "price": 15.49},
]

# Define the route for getting products
@router.get("/products/", response_model=List[Product])
async def get_products():
    return sample_products        

@router.get("/products/", response_model=List[Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = get_products(db=db, skip=skip, limit=limit)  # Call correct function
    return products

@router.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db=db, product_id=product_id)  # Call correct function
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/products/", response_model=Product)
def create_product_view(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        return create_product(db=db, product=product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating product: {e}")

@router.put("/products/{product_id}", response_model=Product)
def update_product_view(
    product_id: int, 
    product: ProductUpdate, 
    db: Session = Depends(get_db)
):
    # Attempt to update the product using the provided ID and update data
    db_product = update_product(db=db, product_id=product_id, product=product)
    
    # If the product does not exist, raise a 404 error
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Return the updated product
    return db_product

@router.delete("/products/{product_id}", response_model=bool)
def delete_product_view(product_id: int, db: Session = Depends(get_db)):
    success = delete_product(db=db, product_id=product_id)  # Call correct function
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return success
