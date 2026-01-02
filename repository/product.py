from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database.models.product import ProductDB


class ProductRepository:

    def get_by_id(self, db: Session, product_id: int):
        return db.get(ProductDB, product_id)

    def create(self, db: Session, product: ProductDB) -> ProductDB:
        try:
            db.add(product)
            db.commit()
            db.refresh(product)
            return product
        except SQLAlchemyError:
            db.rollback()
            raise

    def delete(self, db: Session, product: ProductDB):
        db.delete(product)
        db.commit()
