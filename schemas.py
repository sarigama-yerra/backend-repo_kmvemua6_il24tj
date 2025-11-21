"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal, Dict, Any

# Example schemas (left for reference)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Portfolio-specific schemas
class Contactsubmission(BaseModel):
    """
    Contact form submissions
    Collection: "contactsubmission"
    """
    name: str = Field(..., min_length=2)
    email: EmailStr
    subject: str = Field(..., min_length=2)
    message: str = Field(..., min_length=5)

class Analyticsevent(BaseModel):
    """
    Analytics events for engagement tracking
    Collection: "analyticsevent"
    """
    type: Literal["page_view", "section_view", "click"]
    label: Optional[str] = Field(None, description="Button label, section id, or page name")
    meta: Optional[Dict[str, Any]] = Field(default=None, description="Any additional data such as path, viewport, etc.")
