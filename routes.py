from fastapi import APIRouter, HTTPException

from schemas import UserCreate, StandardResponse, ErrorResponse
from services import UserService

user_router = APIRouter(prefix="/user")
product_router = APIRouter(prefix="/product")
category_router = APIRouter(prefix="/category")
order_router = APIRouter(prefix="/order")
review_router = APIRouter(prefix="/review")


@user_router.post("/create", response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Creates a new user")
async def create_user(user: UserCreate):
    try:
        await UserService.create_user(user)
        return StandardResponse(message="User created successfully")
    except Exception as error:
        raise HTTPException(400, detail=str(error))
    
@user_router.delete("/delete/{user_id}", response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Deletes a user")
async def delete_user(user_id: int):
    try:
        await UserService.delete_user(user_id)
        return StandardResponse(message="User deleted successfully")
    except Exception as e:
        raise HTTPException(400, detail=str(e))