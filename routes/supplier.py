from fastapi import APIRouter, Depends, Query, status, HTTPException
import logging
from schemas.supplier import SupplierCreate, SupplierRead, SupplierPatch
from schemas.common import PaginatedResponse
from services.supplier import SupplierService
from database.dependencies import get_db
from repository.supplier import SupplierRepository

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)
logger = logging.getLogger("supplier_routes")

def get_supplier_service(
    db=Depends(get_db),
) -> SupplierService:
    repository = SupplierRepository(db)
    return SupplierService(repository)


@router.get("/", response_model=PaginatedResponse[SupplierRead])
def list_suppliers(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    order: str = Query("name", pattern="^(name|email|company)$"),
    direction: str = Query("asc", pattern="^(asc|desc)$"),
    service: SupplierService = Depends(get_supplier_service),
):
    return service.get_suppliers(
        page=page,
        page_size=page_size,
        order=order,
        direction=direction,
    )


@router.get("/{supplier_id}", response_model=SupplierRead)
def get_supplier(
    supplier_id: int,
    service: SupplierService = Depends(get_supplier_service),
):
    try:
        return service.get_supplier(supplier_id)
    except ValueError as e:
        logger.error(f"Error fetching supplier {supplier_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=SupplierRead, status_code=201)
def create_supplier(
    supplier: SupplierCreate,
    service: SupplierService = Depends(get_supplier_service),
):
    try:
        return service.create_supplier(supplier)
    except Exception as e:
        logger.error(f"Error creating supplier: {e}")
        raise HTTPException(status_code=400, detail="Error creating supplier")


@router.patch("/{supplier_id}", response_model=SupplierRead)
def patch_supplier(
    supplier_id: int,
    supplier: SupplierPatch,
    service: SupplierService = Depends(get_supplier_service),
):
    try:
        return service.patch_supplier(supplier_id, supplier)
    except ValueError as e:
        logger.error(f"Error updating supplier {supplier_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: int,
    service: SupplierService = Depends(get_supplier_service),
):
    try:
        service.delete_supplier(supplier_id)
        return None
    except ValueError as e:
        logger.error(f"Error deleting supplier {supplier_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))
