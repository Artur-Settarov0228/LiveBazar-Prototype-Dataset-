from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, DECIMAL, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import Base
import enum


class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(350), index=True)   
    address = Column(String(500))
    phone = Column(String(20))
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime)
    products = relationship("Product", back_populates="shop")


class Category(Base):
    __annotations__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    praedicates = relationship("Product", back_populates="category")
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, ForeignKey("shops.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String(150), nullable=False)
    description = Column(Text)
    price = Column(DECIMAL(10,2), nullable=False)
    size = Column(String(20))
    color = Column(String(50))
    stock = Column(Integer, default=0)

    shop = relationship("Shop", back_populates="products")
    category = relationship("Category", back_populates="products")


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String, unique=True, index=True)
    phone = Column(String(20))
    address = Column(String(500))
    orders = relationship("Order", back_populates="customer")


class OrderStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10,2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")    