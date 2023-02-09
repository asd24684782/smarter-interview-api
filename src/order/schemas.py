from pydantic import BaseModel, validator
from typing import Optional, List, Union
from datetime import datetime

class OrderSchema(BaseModel):
    order_id        : Optional[str]
    customer_name   : str
    custmer_id      : str
    purchase_time   : Optional[datetime]
    
    @validator('customer_name')
    def customer_name_rules(cls, v, values, **kwargs):
        if len(v) > 10:
            raise ValueError('customer name too long')
        return v


class ItemSchema(BaseModel):
    order_id          : str
    product_name      : str
    product_id        : str
    amount            : int
    price             : int

    @validator('product_name')
    def product_name_rules(cls, v, values, **kwargs):
        if len(v) > 10:
            raise ValueError('product name too long')
        return v


class OrderItemCreateBody(BaseModel):
    order  : OrderSchema
    items  : Optional[List[Union[ItemSchema, None]]]