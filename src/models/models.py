from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy import String, ForeignKey, DateTime, func, Boolean, Numeric

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(timezone.utc))

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String())
    price: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column()
    category: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(timezone.utc))

class CartItem(Base):
    __tablename__ = "cart_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(timezone.utc))

    product: Mapped["Product"] = relationship("Product")

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    total_amount: Mapped[Numeric] = mapped_column(Numeric(10, 2))
    address: Mapped[str] = mapped_column(String(150))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(timezone.utc))

    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")
    user: Mapped["User"] = relationship("User", back_populates="orders")

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column()
    price_at_order: Mapped[Numeric] = mapped_column(Numeric(10, 2))

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product")