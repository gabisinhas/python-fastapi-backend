from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from sqlalchemy.exc import SQLAlchemyError
from database.models.supplier import SupplierDB

class SupplierRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, supplier_id: int) -> Optional[SupplierDB]:
        return self.db.query(SupplierDB).filter(SupplierDB.id == supplier_id).first()

    def get_all(
        self,
        *,
        page: int,
        page_size: int,
        order: str = "name",
        direction: str = "asc",
    ) -> Tuple[List[SupplierDB], int]:

        query = self.db.query(SupplierDB)

        order_map = {
            "name": SupplierDB.name,
            "email": SupplierDB.email,
            "company": SupplierDB.company,
        }

        column = order_map.get(order, SupplierDB.name)

        if direction == "desc":
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

        total = query.count()

        suppliers = query.offset((page - 1) * page_size).limit(page_size).all()

        return suppliers, total

    def get_by_email(self, email: str) -> Optional[SupplierDB]:
        return self.db.query(SupplierDB).filter(SupplierDB.email == email).first()

    def create(self, supplier: SupplierDB) -> SupplierDB:
        try:
            self.db.add(supplier)
            self.db.commit()
            self.db.refresh(supplier)
            return supplier
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, supplier: SupplierDB) -> None:
        try:
            self.db.delete(supplier)
            self.db.commit()
        except SQLAlchemyError:
            self.db.rollback()
            raise
