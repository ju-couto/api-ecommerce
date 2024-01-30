from fastapi import APIRouter, HTTPException

from schemas import Product, StandardResponse, ErrorResponse
from services.products import ProductService


product_router = APIRouter(prefix="/products")


@product_router.post('', response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Creates a product")
async def create_product(product: Product):
    try:
        await ProductService.create_product(product)
        return StandardResponse(message="Product created successfully")
    except Exception as error:
        raise HTTPException(400, detail=str(error))


@product_router.delete("/{product_id}", response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Deletes a product")
async def delete_product(product_id: int):
    try:
        await ProductService.delete_product(product_id)
        return StandardResponse(message="Product deleted successfully")
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@product_router.get("/{product_id}", responses={400: {"model": ErrorResponse}}, description="Returns a product")
async def get_product(product_id: int):
    try:
        product = await ProductService.get_product(product_id)
        return product
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@product_router.get("", responses={400: {"model": ErrorResponse}}, description="Returns all products")
async def get_products():
    try:
        products = await ProductService.get_products()
        return products
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@product_router.get("/by_category/{category_id}", responses={400: {"model": ErrorResponse}}, description="Returns all products by category")
async def get_products_by_category(category_id: int):
    try:
        products = await ProductService.get_products_by_category(category_id)
        return products
    except Exception as e:
        raise HTTPException(400, detail=str(e))


@product_router.put("/{product_id}", response_model=StandardResponse, responses={400: {"model": ErrorResponse}}, description="Updates a product")
async def update_product(product_id: int, product: Product):
    try:
        await ProductService.update_product(product_id, product)
        return StandardResponse(message="Product updated successfully")
    except Exception as e:
        raise HTTPException(400, detail=str(e))
