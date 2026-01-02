from fastapi import FastAPI
from routes.supplier import router as supplier_router
from routes.product import router as product_router
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Access /docs for API documentation."}

app.include_router(supplier_router, prefix="/suppliers", tags=["Suppliers"])
app.include_router(product_router, prefix="/products", tags=["Products"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
