from pydantic import BaseModel, EmailStr, constr
from typing import Optional, Dict
from datetime import datetime
from uuid import UUID
from decimal import Decimal
import enum



# User Schemas
class UserCreate(BaseModel):
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    phone: Optional[constr(max_length=15)]
    password: str
    role: Optional[str] = "Customer"

class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[constr(max_length=15)]
    password: Optional[str]
    role: Optional[str]

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    phone: Optional[str]
    active: bool
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        
      
        
 # # Media Schemas       
class MediaBase(BaseModel):
    filename: str
    file_url: str
    file_size: int
    file_type: str

class MediaCreate(MediaBase):
    pass

class Media(MediaBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True



# Product Status Enum
class ProductStatus(str, enum.Enum):
    ACTIVE = 'Active'
    DRAFT = 'Draft'

class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    short_description: Optional[str]
    price: Optional[Decimal]
    cost: Optional[Decimal]
    quantity: Optional[int]
    sku: Optional[str]
    slug: Optional[str]
    seo_title: Optional[str]
    seo_description: Optional[str]
    status: Optional[str] = "Draft"

class Product(ProductBase):
    id: int
    created_at: str  # String format for datetime
    updated_at: str  # String format for datetime
    
class ProductCreate(ProductBase):
    pass  # Inherit fields from ProductBase

    class Config:
        orm_mode = True
        # This will allow FastAPI to automatically convert datetime to string
        json_encoders = {
            datetime: lambda v: v.isoformat(),  # Converts datetime to ISO format string
        }

# Define ProductUpdate schema
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    price: Optional[Decimal] = None
    cost: Optional[Decimal] = None
    quantity: Optional[int] = None
    sku: Optional[str] = None
    slug: Optional[str] = None
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    status: Optional[str] = None
        
# # Product Variant Schemas
# class ProductVariantBase(BaseModel):
#     product_id: int
#     name: str
#     sku: Optional[str]
#     weight: Optional[float]
#     option_1_name: Optional[str]
#     option_1_value: Optional[str]
#     option_2_name: Optional[str]
#     option_2_value: Optional[str]
#     option_3_name: Optional[str]
#     option_3_value: Optional[str]
#     price: float
#     compare_price: Optional[float]
#     continue_selling: Optional[bool] = False
#     quantity: Optional[int] = 0

# class ProductVariantCreate(ProductVariantBase):
#     pass

# class ProductVariantUpdate(BaseModel):
#     name: Optional[str]
#     sku: Optional[str]
#     weight: Optional[float]
#     option_1_name: Optional[str]
#     option_1_value: Optional[str]
#     option_2_name: Optional[str]
#     option_2_value: Optional[str]
#     option_3_name: Optional[str]
#     option_3_value: Optional[str]
#     price: Optional[float]
#     compare_price: Optional[float]
#     continue_selling: Optional[bool]
#     quantity: Optional[int]

# class ProductVariantResponse(ProductVariantBase):
#     id: int
#     created_at: datetime
#     updated_at: datetime
#     deleted_at: Optional[datetime]

#     class Config:
#         orm_mode = True


