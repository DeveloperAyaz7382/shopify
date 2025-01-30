from pydantic import BaseModel, EmailStr, Field, constr
from typing import Optional, Dict
from datetime import datetime
from uuid import UUID
from decimal import Decimal
import enum
from pydantic import BaseModel, condecimal, conint


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
    
    
    
#  # Schema definitions
# class ProductVariantBase(BaseModel):
#     product_id: int
#     name: str
#     sku: Optional[str] = None
#     weight: Optional[float] = None
#     option_1_name: Optional[str] = None
#     option_1_value: Optional[str] = None
#     option_2_name: Optional[str] = None
#     option_2_value: Optional[str] = None
#     option_3_name: Optional[str] = None
#     option_3_value: Optional[str] = None
#     price: float = Field(..., ge=0)
#     compare_price: Optional[float] = None
#     continue_selling: bool = False
#     image_id: Optional[int] = None
#     quantity: int = Field(0, ge=0)

# class ProductVariantCreate(ProductVariantBase):
#     pass

# class ProductVariantUpdate(BaseModel):
#     name: Optional[str] = None
#     sku: Optional[str] = None
#     weight: Optional[float] = None
#     option_1_name: Optional[str] = None
#     option_1_value: Optional[str] = None
#     option_2_name: Optional[str] = None
#     option_2_value: Optional[str] = None
#     option_3_name: Optional[str] = None
#     option_3_value: Optional[str] = None
#     price: Optional[float] = Field(None, ge=0)
#     compare_price: Optional[float] = None
#     continue_selling: Optional[bool] = None
#     image_id: Optional[int] = None
#     quantity: Optional[int] = Field(None, ge=0)

# class ProductVariantResponse(ProductVariantBase):
#     id: int
#     created_at: str
#     updated_at: str

#     class Config:
#         orm_mode = True


# ✅ Base Schema
class ProductVariantBase(BaseModel):
    name: str
    sku: Optional[str] = None
    weight: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    price: condecimal(max_digits=10, decimal_places=2)
    options: Optional[Dict[str, str]] = None  # JSON for variant options
    continue_selling: Optional[bool] = False
    image_id: Optional[int] = None
    quantity: conint(ge=0)

# ✅ Schema for Creating a Product Variant
class ProductVariantCreate(ProductVariantBase):
    product_id: int

# ✅ Schema for Updating a Product Variant
class ProductVariantUpdate(ProductVariantBase):
    pass

# ✅ Schema for Returning Data
class ProductVariantResponse(ProductVariantBase):
    id: int
    product_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True