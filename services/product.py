from sqlalchemy.orm import Session
from decimal import Decimal

from database.models.product import ProductDB
from repository.product import ProductRepository
from schemas.product import ProductCreate, ProductPatch


class ProductService:
    def __init__(self):
        self.repo = ProductRepository()

    def get_product(self, db: Session, product_id: int) -> ProductDB:
        product = self.repo.get_by_id(db, product_id)
        if not product:
            raise ValueError(f"Product with id {product_id} not found")
        return product

    def create_product(self, db: Session, product_data: ProductCreate) -> ProductDB:
        # Business rule: values cannot be negative
        if product_data.quantity_in_stock < 0:
            raise ValueError("Quantity in stock cannot be negative.")
        if product_data.quantity_sold < 0:
            raise ValueError("Quantity sold cannot be negative.")
        if product_data.unit_price < 0:
            raise ValueError("Unit price cannot be negative.")

        # Business rule: quantity_sold cannot exceed quantity_in_stock
        if product_data.quantity_sold > product_data.quantity_in_stock:
            raise ValueError("Quantity sold cannot exceed quantity in stock.")

        # Business rule: supplier must exist
        from database.models.supplier import SupplierDB
        supplier = db.get(SupplierDB, product_data.supplier_id)
        if not supplier:
            raise ValueError(f"Supplier with id {product_data.supplier_id} does not exist.")

        revenue = Decimal(product_data.quantity_sold) * Decimal(product_data.unit_price)
        product = ProductDB(
            name=product_data.name,
            quantity_in_stock=product_data.quantity_in_stock,
            quantity_sold=product_data.quantity_sold,
            unit_price=product_data.unit_price,
            revenue=revenue,
            supplier_id=product_data.supplier_id,
        )
        return self.repo.create(db, product)

    def update_product(self, db: Session, product_id: int, patch_data: ProductPatch) -> ProductDB:
        product = self.get_product(db, product_id)

        updates = patch_data.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(product, field, value)

        # Business rule: values cannot be negative
        if product.quantity_in_stock < 0:
            raise ValueError("Quantity in stock cannot be negative.")
        if product.quantity_sold < 0:
            raise ValueError("Quantity sold cannot be negative.")
        if product.unit_price < 0:
            raise ValueError("Unit price cannot be negative.")

        # Business rule: quantity_sold cannot exceed quantity_in_stock
        if (
            ("quantity_sold" in updates or "quantity_in_stock" in updates)
            and product.quantity_sold > product.quantity_in_stock
        ):
            raise ValueError("Quantity sold cannot exceed quantity in stock.")

        if "quantity_sold" in updates or "unit_price" in updates:
            product.revenue = Decimal(product.quantity_sold) * Decimal(product.unit_price)

        return self.repo.create(db, product)

    def delete_product(self, db: Session, product_id: int):
        product = self.get_product(db, product_id)
        self.repo.delete(db, product)
        return {"detail": "Product deleted successfully"}
