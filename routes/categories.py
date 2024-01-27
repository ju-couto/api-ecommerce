from fastapi import APIRouter, HTTPException

from schemas import Category, StandardResponse, ErrorResponse
from services.categories import CategoryService


category_router = APIRouter(prefix="/categories")


@category_router.post('', response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Creates a category")
async def create_category(category: Category):
    try:
        await CategoryService.create_category(category)
        return StandardResponse(message="Category created successfully")
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@category_router.delete("/{category_id}", response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Deletes a category")
async def delete_category(category_id: int):
    try:
        await CategoryService.delete_category(category_id)
        return StandardResponse(message="Category deleted successfully")
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@category_router.get("/{category_id}", responses={400: {"model": ErrorResponse}}, description="Returns a category")
async def get_category(category_id: int):
    try:
        category = await CategoryService.get_category(category_id)
        return category
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@category_router.get("", responses={400: {"model": ErrorResponse}}, description="Returns all categories")
async def get_categories():
    try:
        users = await CategoryService.get_categories()
        return users
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@category_router.put("/{category_id}", response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Updates a category")
async def update_category(category_id: int, category: Category):
    try:
        await CategoryService.update_category(category_id, category)
        return StandardResponse(message="Category updated successfully")
    except Exception as e:
        raise HTTPException(400, detail=str(e))
