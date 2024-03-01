from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    address: str

class UserUpdate(BaseModel):
    name: str
    email: str
    address: str


class StandardResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    detail: str

class Product(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int
    image_url: str
    
class ProductUpdate(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int
    image_url: str
    
class Category(BaseModel):
    name: str


class Order(BaseModel):
    user_id: int
    status: str
    shipping_cost: float
    total_amount: float

class OrderUpdate(BaseModel):
    status: str
    shipping_cost: float
    
class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderInput(BaseModel):
    order: Order
    order_items: list[OrderItem]
    
class OrderUpdateInput(BaseModel):
    order : OrderUpdate    
    order_items: list[OrderItem]

class Review(BaseModel):
    product_id: int
    user_id: int
    rating: int
    comment: str
