from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional


class SupplierBase(BaseModel):
    name: str = Field(min_length=3, max_length=20)
    company: str = Field(min_length=3, max_length=20)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=15)


class SupplierCreate(SupplierBase):
    pass


class SupplierPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=20)
    company: Optional[str] = Field(None, min_length=3, max_length=20)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=7, max_length=15)


class SupplierRead(SupplierBase):
    id: int

