from fastapi import APIRouter, HTTPException

from schemas import Order, StandardResponse, ErrorResponse,OrderInput
from services.orders import OrderService

order_router = APIRouter(prefix="/orders")


@order_router.post('', response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Creates a new order")
async def create_order(order_input: OrderInput):
    try:
        await OrderService.create_order(order_input.order, order_input.order_items)
        return StandardResponse(message="Order created successfully")
    except Exception as error:
        raise HTTPException(400, detail=str(error))


# @user_router.delete("/{user_id}", response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Deletes a user")
# async def delete_user(user_id: int):
#     try:
#         await UserService.delete_user(user_id)
#         return StandardResponse(message="User deleted successfully")
#     except Exception as e:
#         raise HTTPException(400, detail=str(e))


@order_router.get("/{order_id}", responses={400: {"model": ErrorResponse}}, description="Returns a order")
async def get_order(order_id: int):
    try:
        order = await OrderService.get_order(order_id)
        return order
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@order_router.get("", responses={400: {"model": ErrorResponse}}, description="Returns all orders")
async def get_orders():
    try:
        orders = await OrderService.get_orders()
        return orders
    except Exception as e:
        raise HTTPException(400, detail=str(e))


# @user_router.put("/{user_id}", response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Updates a user")
# async def update_user(user_id: int, user: UserUpdate):
#     try:
#         await UserService.update_user(user_id, user)
#         return StandardResponse(message="User updated successfully")
#     except Exception as e:
#         raise HTTPException(400, detail=str(e))
