from pydantic import BaseModel
from typing import List


class GeographySchema(BaseModel):
    id: int
    short_name: str
    name: str


class EntrySchema(BaseModel):
    id: str
    unit: str
    geography_id: int
    product_name: str

    class Config:
        orm_mode = True


class IndicatorSchema(BaseModel):
    id: int
    method: str
    category: str
    indicator: str
    unit: str

    class Config:
        orm_mode = True


class ImpactSchema(BaseModel):
    id: int
    indicator_id: int
    entry_id: int
    coefficient: float

    class Config:
        orm_mode = True


class ImpactSchemaExtended(BaseModel):
    id: int
    indicator: IndicatorSchema
    entry: EntrySchema
    coefficient: float


class EntrySchemaExtended(BaseModel):
    id: str
    product_name: str
    geography: GeographySchema
    unit: str
    impact: List[ImpactSchema]

    class Config:
        orm_mode = True
