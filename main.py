from fastapi import FastAPI, APIRouter

from routes import user_router, product_router, category_router, order_router, review_router
app = FastAPI()
router = APIRouter()

@router.get("/")
def first_api():
    return {"message": "Hello World!"}

app.include_router(router=router, prefix="/api/v1")
app.include_router(router=user_router)
app.include_router(router=product_router)
app.include_router(router=category_router)
app.include_router(router=order_router)
app.include_router(router=review_router)
