from fastapi import APIRouter, Depends, HTTPException
import logging
from sqlalchemy.orm import Session
from database.dependencies import get_db
from services.product import ProductService
from schemas.product import ProductCreate, ProductPatch, ProductRead

router = APIRouter(prefix="/products", tags=["Products"])
service = ProductService()
logger = logging.getLogger("product_routes")

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        return service.get_product(db, product_id)
    except ValueError as e:
        logger.error(f"Error fetching product {product_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    return service.create_product(db, product)

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, patch: ProductPatch, db: Session = Depends(get_db)):
    try:
        return service.update_product(db, product_id, patch)
    except ValueError as e:
        logger.error(f"Error updating product {product_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        return service.delete_product(db, product_id)
    except ValueError as e:
        logger.error(f"Error deleting product {product_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))
