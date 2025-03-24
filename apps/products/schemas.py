from ninja_schema import ModelSchema, Schema

class ProductResponseSchema(Schema):
    product: str
    unit_price: float
    stock: int