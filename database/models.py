from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    address = Column(String(255))
    role = Column(String(50), default="user")
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    description = Column(String)
    price = Column(DECIMAL(10,2))
    stock_quantity = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    products = relationship("Product", backref="category")
    
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    order_status = Column(String(50))
    total_amount = Column(DECIMAL(10,2))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(DECIMAL(10,2))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)
    comment = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)