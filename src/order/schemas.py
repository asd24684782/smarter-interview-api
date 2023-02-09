from pydantic import BaseModel, validator
from typing import Optional, List, Union
from datetime import datetime

class OrderPostSchema(BaseModel):
    customer_name   : str
    customer_id     : str
    
    @validator('customer_name')
    def customer_name_rules(cls, v, values, **kwargs):
        if len(v) > 10:
            raise ValueError('customer name too long')
        return v


class OrderResponseSchema(BaseModel):
    order_id        : Optional[str]
    customer_name   : str
    customer_id     : str
    purchase_time   : Optional[datetime]
    

class ItemPostSchema(BaseModel):
    product_name      : str
    product_id        : str
    amount            : int
    price             : int

    @validator('product_name')
    def product_name_rules(cls, v, values, **kwargs):
        if len(v) > 10:
            raise ValueError('product name too long')
        return v


class ItemResponseSchema(BaseModel):
    product_name      : str
    product_id        : str
    amount            : int
    price             : int



class OrderItemCreateBody(BaseModel):
    order  : OrderPostSchema
    items  : Optional[List[Union[ItemPostSchema, None]]]


class OrderItemResponseSchemra(BaseModel):
    order  : OrderResponseSchema
    items  : List[ItemResponseSchema]
