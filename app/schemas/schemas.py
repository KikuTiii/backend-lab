from pydantic import BaseModel, Field


class OrderInput(BaseModel):
    customer_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0)

class OrderOutput(OrderInput):
    id: int
    status: str
