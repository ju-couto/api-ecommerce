from fastapi import APIRouter, HTTPException

from schemas import UserCreate, UserUpdate, StandardResponse, ErrorResponse
from services.users import UserService

user_router = APIRouter(prefix="/users")


@user_router.post('', response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Creates a new user")
async def create_user(user: UserCreate):
    try:
        await UserService.create_user(user)
        return StandardResponse(message="User created successfully")
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@user_router.delete("/{user_id}", response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Deletes a user")
async def delete_user(user_id: int):
    try:
        await UserService.delete_user(user_id)
        return StandardResponse(message="User deleted successfully")
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@user_router.get("/{user_id}", responses={400: {"model": ErrorResponse}}, description="Returns a user")
async def get_user(user_id: int):
    try:
        user = await UserService.get_user(user_id)
        return user
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@user_router.get("", responses={400: {"model": ErrorResponse}}, description="Returns all users")
async def get_users():
    try:
        users = await UserService.get_users()
        return users
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@user_router.put("/{user_id}", response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Updates a user")
async def update_user(user_id: int, user: UserUpdate):
    try:
        await UserService.update_user(user_id, user)
        return StandardResponse(message="User updated successfully")
    except Exception as e:
        raise HTTPException(400, detail=str(e))
