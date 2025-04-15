from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.schemas.schemas import (
    ProductSchema,
    CartItemSchema,
    CartItemResponse,
    OrderSchema,
    OrderResponse,
)
from src.models.models import Product, CartItem, Product, Order
from src.database.db import get_db
from src.repository.repository import (
    add_cart_item,
    get_cart_items_by_user,
    create_order,
)
from src.services.auth import auth_service

router = APIRouter(prefix="/app", tags=["app"])


@router.get("/products", response_model=list[ProductSchema])
async def get_products(db: AsyncSession = Depends(get_db)):
    stmt = select(Product)
    products = await db.execute(stmt)
    products = products.scalars().all()
    return products


@router.post("/products", response_model=ProductSchema)
async def create_product(body: ProductSchema, db: AsyncSession = Depends(get_db)):
    new_product = Product(**body.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


@router.post("/cart", response_model=CartItemResponse)
async def add_to_cart(body: CartItemSchema, db: AsyncSession = Depends(get_db)):
    existing_item = await db.execute(
        select(CartItem).filter_by(user_id=body.user_id, product_id=body.product_id)
    )
    existing_item = existing_item.scalar_one_or_none()

    if existing_item:
        existing_item.quantity += body.quantity
        db.add(existing_item)
        await db.commit()
        await db.refresh(existing_item)
        return existing_item

    cart_item = await add_cart_item(
        body, db
    )
    return cart_item


@router.get("/cart/{user_id}", response_model=list[CartItemResponse])
async def get_cart_items(user_id: int, db: AsyncSession = Depends(get_db)):
    cart_items = await get_cart_items_by_user(user_id, db)
    return cart_items


@router.post("/order", response_model=OrderResponse)
async def create_order_route(
    body: OrderSchema, user_id: int, db: AsyncSession = Depends(get_db)
):
    order = await create_order(user_id, body, db)
    return order


@router.get("/orders/{user_id}", response_model=list[OrderResponse])
async def get_user_orders(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(Order).filter_by(user_id=user_id)
    orders = await db.execute(stmt)
    orders = orders.scalars().all()
    return orders
