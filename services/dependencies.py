from fastapi import Depends
from sqlalchemy.orm import Session

from database.dependencies import get_db
from services.supplier import SupplierService
from services.product import ProductService
from repository.supplier import SupplierRepository
from repository.product import ProductRepository


def get_supplier_service(
    db: Session = Depends(get_db),
) -> SupplierService:
    supplier_repository = SupplierRepository(db)
    return SupplierService(supplier_repository)


def get_product_service(
    db: Session = Depends(get_db),
) -> ProductService:
    product_repository = ProductRepository(db)
    supplier_repository = SupplierRepository(db)

    return ProductService(
        product_repository,
        supplier_repository,
    )
