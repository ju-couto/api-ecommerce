from fastapi import APIRouter, HTTPException

from schemas import Order, StandardResponse, ErrorResponse, OrderInput, OrderUpdateInput
from services.orders import OrderService

order_router = APIRouter(prefix="/orders")


@order_router.post('', response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Creates a new order")
async def create_order(order_input: OrderInput):
    try:
        await OrderService.create_order(order_input.order, order_input.order_items)
        return StandardResponse(message="Order created successfully")
    except Exception as error:
        raise HTTPException(400, detail=str(error))


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


@order_router.get('/user/{user_id}', responses={400: {"model": ErrorResponse}}, description="Returns all orders by user")
async def get_orders_by_user(user_id: int):
    try:
        orders = await OrderService.get_orders_by_user(user_id)
        return orders
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@order_router.get('/status/{status}', responses={400: {"model": ErrorResponse}}, description="Returns all orders by status")
async def get_orders_by_status(status: str):
    try:
        orders = await OrderService.get_orders_by_status(status)
        return orders
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@order_router.get('/user/{user_id}/status/{status}', responses={400: {"model": ErrorResponse}}, description="Returns all orders by user and status")
async def get_orders_by_user_and_status(user_id: int, status: str):
    try:
        orders = await OrderService.get_orders_by_user_and_status(user_id, status)
        return orders
    except Exception as e:
        raise HTTPException(400, detail=str(e))
    
@order_router.put("/{order_id}", response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Updates a order")
async def update_order(order_id: int, order: OrderUpdateInput):
    try:
        await OrderService.update_order(order_id, order)
        return StandardResponse(message="Order updated successfully")
    except Exception as e:
        raise HTTPException(400, detail=str(e))
