from pydantic import BaseModel

class PurchaseRequest(BaseModel):
    product_id: int
