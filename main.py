import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse
from routes.users import user_router
from routes.products import product_router
from routes.categories import category_router
from routes.orders import order_router


app = FastAPI()
router = APIRouter()

@router.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")

app.include_router(router=router)
app.include_router(router=user_router)
app.include_router(router=product_router)
app.include_router(router=category_router)
app.include_router(router=order_router)
# app.include_router(router=review_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)