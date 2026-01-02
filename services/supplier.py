from fastapi import HTTPException, status
from repository.supplier import SupplierRepository
from schemas.supplier import SupplierCreate, SupplierPatch
from database.models.supplier import SupplierDB


class SupplierService:
    def __init__(self, repository: SupplierRepository):
        self.repository = repository

    def get_suppliers(
        self,
        *,
        page: int = 1,
        page_size: int = 10,
        order: str = "name",
        direction: str = "asc",
    ):
        if page < 1 or page_size < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid pagination parameters"
            )

        suppliers, total = self.repository.get_all(
            page=page,
            page_size=page_size,
            order=order,
            direction=direction,
        )

        return {
            "items": suppliers,
            "total": total,
            "page": page,
            "page_size": page_size,
            "pages": (total + page_size - 1) // page_size,
        }

    def get_supplier(self, supplier_id: int):
        supplier = self.repository.get_by_id(supplier_id)
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found"
            )
        return supplier

    def create_supplier(self, data: SupplierCreate):
        if self.repository.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        
        import re
        phone_pattern = r"^\+?\d{7,15}$"
        if not re.match(phone_pattern, data.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone number format. Must be 7-15 digits, optional +."
            )

        supplier = SupplierDB(**data.dict())
        return self.repository.create(supplier)

    def patch_supplier(self, supplier_id: int, data: SupplierPatch):
        supplier = self.repository.get_by_id(supplier_id)
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found"
            )

        updates = data.dict(exclude_unset=True)
        
        import re
        if "phone" in updates:
            phone_pattern = r"^\+?\d{7,15}$"
            if not re.match(phone_pattern, updates["phone"]):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid phone number format. Must be 7-15 digits, optional +."
                )

        for field, value in updates.items():
            setattr(supplier, field, value)

        try:
            self.repository.db.commit()
            self.repository.db.refresh(supplier)
            return supplier
        except Exception:
            self.repository.db.rollback()
            raise

    def delete_supplier(self, supplier_id: int):
        supplier = self.repository.get_by_id(supplier_id)
        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found"
            )

        if supplier.products:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete supplier with products"
            )

        self.repository.delete(supplier)
