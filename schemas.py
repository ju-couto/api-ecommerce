from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    address: str


class StandardResponse(BaseModel):
    message: str


class AlternativeResponse(StandardResponse):
    detail: str

class ErrorResponse(BaseModel):
    detail: str

class Product(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int
    category_id: int


class Category(BaseModel):
    name: str


class Order(BaseModel):
    user_id: int
    order_status: str
    total_amount: float


class OrderItem(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float


class Review(BaseModel):
    product_id: int
    user_id: int
    rating: int
    comment: str
