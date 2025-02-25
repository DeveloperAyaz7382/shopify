from decimal import Decimal
from typing import Text
from sqlalchemy import DECIMAL, CheckConstraint, Column, BigInteger, LargeBinary, String, Numeric, Boolean, Integer, ForeignKey, DateTime, JSON, UUID
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from datetime import datetime
import enum
import uuid
from sqlalchemy import Text

Base = declarative_base()

# Enum for Product Status
class ProductStatus(str, enum.Enum):
    ACTIVE = 'Active'
    DRAFT = 'Draft'

# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255))
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(15))
    email_verified_at = Column(DateTime)
    password = Column(String(255), nullable=False)
    remember_token = Column(String(100))
    active = Column(Boolean, default=True, nullable=False)
    role = Column(String(255), default="Customer", nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

    __table_args__ = (
        CheckConstraint("role IN ('Admin', 'Customer', 'Supplier', 'Staff')", name="users_role_check"),
    )

# Media Model
class Media(Base):
    __tablename__ = "media"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_url = Column(Text, index=True)
    file_size = Column(Integer)
    file_type = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)  

    # Back reference to ProductVariant (NO delete-orphan)
    product_variants = relationship("ProductVariant", back_populates="image")

# Product Model
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    short_description = Column(String)
    price = Column(DECIMAL(precision=10, scale=2))
    cost = Column(DECIMAL(precision=10, scale=2))
    quantity = Column(Integer)
    sku = Column(String)
    slug = Column(String)
    seo_title = Column(String)
    seo_description = Column(String)
    status = Column(String, default="Draft")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship with ProductVariant
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Product(name={self.name}, sku={self.sku})>"

class ProductVariant(Base):
    __tablename__ = "product_variants"

    id = Column(BigInteger, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id', ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    sku = Column(String(255), unique=True, nullable=True)  # Ensuring uniqueness for better SKU management
    weight = Column(Numeric(10, 2), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    options = Column(JSON, nullable=True)  # Stores variant options like {"color": "red", "size": "M"}
    continue_selling = Column(Boolean, default=False)
    image_id = Column(BigInteger, ForeignKey("media.id", ondelete="SET NULL"), nullable=True)
    quantity = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="variants")
    image = relationship("Media", back_populates="product_variants")

    __table_args__ = (
        CheckConstraint("quantity >= 0", name="product_variant_quantity_check"),
        CheckConstraint("price >= 0", name="product_variant_price_check"),
    )

    def __repr__(self):
        return f"<ProductVariant(name={self.name}, sku={self.sku}, price={self.price})>"