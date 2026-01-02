from pydantic import BaseModel, Field, ConfigDict
from pydantic.types import condecimal
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(min_length=3, max_length=30)
    quantity_in_stock: int = Field(ge=0)
    quantity_sold: int = Field(ge=0)
    unit_price: condecimal(max_digits=8, decimal_places=2, gt=0)


class ProductCreate(ProductBase):
    supplier_id: int


class ProductPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=30)
    quantity_in_stock: Optional[int] = Field(None, ge=0)
    quantity_sold: Optional[int] = Field(None, ge=0)
    unit_price: Optional[
        condecimal(max_digits=8, decimal_places=2, gt=0)
    ] = None


class ProductRead(ProductBase):
    id: int
    revenue: condecimal(max_digits=20, decimal_places=2)
    supplier_id: int

