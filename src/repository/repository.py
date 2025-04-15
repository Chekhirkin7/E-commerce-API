from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import User, Order, OrderItem, CartItem, Product
from src.schemas.schemas import (
    UserSchema,
    ProductSchema,
    CartItemSchema,
    OrderSchema,
)


async def get_user_by_email(email: str, db: AsyncSession):
    stmt = select(User).filter_by(email=email)
    user = await db.execute(stmt)
    user = user.scalar_one_or_none()
    return user


async def create_user(body: UserSchema, db: AsyncSession):
    new_user = User(**body.model_dump())
    db.add(new_user)
    await db.commit()
    await db.refresh()
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession):
    user.refresh_token = token
    await db.commit()


async def create_product(body: ProductSchema, db: AsyncSession):
    new_product = Product(**body.model_dump())
    db.add(new_product)
    await db.commit()
    await db.refresh()
    return new_product


async def get_products(db: AsyncSession):
    stmt = select(Product)
    products = await db.execute(stmt)
    products = products.scalars().all()
    return products


async def add_cart_item(body: CartItemSchema, db: AsyncSession):
    new_cart_item = CartItem(**body.model_dump())
    db.add(new_cart_item)
    await db.commit()
    await db.refresh()
    return new_cart_item


async def get_cart_items_by_user(id: int, db: AsyncSession):
    stmt = select(CartItem).filter_by(user_id=id)
    cart_items = await db.execute(stmt)
    cart_items = cart_items.scalars().all()
    return cart_items


async def clear_cart_by_user(user_id: int, db: AsyncSession):
    stmt = select(CartItem).filter_by(user_id=user_id)
    cart_items = await db.execute(stmt)
    cart_items = cart_items.scalars().all()

    for item in cart_items:
        await db.delete(item)

    await db.commit()


async def create_order(id: int, body: OrderSchema, db: AsyncSession):
    items = await get_cart_items_by_user(id, db)

    total_amount = sum(item.price * item.quantity for item in items)

    new_order = Order(user_id=id, total_amount=total_amount, address=body.address)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)

    for item in items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_order=item.price,
        )
        db.add(order_item)

        product = await db.execute(select(Product).filter_by(id=item.product_id))
        product = product.scalar_one_or_none()

        if product:
            product.quantity -= item.quantity
            db.add(product)

    await db.execute(select(CartItem).filter_by(user_id=id))
    await db.commit()
    await db.refresh()

    return new_order
