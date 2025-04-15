from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from decimal import Decimal


class UserSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class ProductSchema(BaseModel):
    name: str = Field(max_length=50)
    description: str
    price: Decimal = Field(ge=0, le=99999999.99, description="Format 000.00")
    quantity: int = Field(ge=1)
    category: str = Field(max_length=50)

    class Config:
        from_attributes = True


class CartItemSchema(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)


class CartItemResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int = Field(ge=1)
    created_at: datetime

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    address: str = Field(max_length=150)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    address: str
    created_at: datetime

    class Config:
        from_attributes = True


class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price_at_order: Decimal

    class Config:
        from_attributes = True
