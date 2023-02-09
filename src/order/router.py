# -*- coding: UTF-8 -*-
import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, status

from order.models import order_db
from order.schemas import OrderSchema, OrderItemCreateBody

# -------------------- global -----------------------------------
router = APIRouter(
    prefix="/order",
    tags=["order"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger()

# ----------------------- api ------------------------------------
@router.get("/{order_id}", response_model=OrderSchema, status_code=status.HTTP_201_CREATED)
async def get_order_by_id(order_id: str):
    try:
        order_tuple = order_db.get_order_by_id(order_id)
        logger.info(order_tuple)
        #order = OrderSchema(**{key: order_tuple[i] for i, key in enumerate(OrderSchema.__fields__.keys())})
        return order_tuple

    except Exception as e:
        return e


@router.post('/')
async def add_order_and_item(order_item_body: OrderItemCreateBody):
    try:
        order = order_item_body.order
        items = order_item_body.items


        now = datetime.now()
        order_id = datetime.strftime(now, '%Y%m%d%H%M%S%f')

        order_tuple = (order_id, order.customer_name, order.customer_id, now)

        item_tuple_list = []
        for item in items:
            item_tuple = (item.product_name, item.product_id, item.amount, item.price, order_id)
            item_tuple_list.append(item_tuple)

        order_db.insert_order_and_items(order_tuple, item_tuple_list)

        return 'OK'

    except Exception as e:
        return e


@router.get('/order/{order_id}/item')
async def get_order_item(order_id: str):
    try:
        item_tuple_list = order_db.get_item_by_order_id(order_id)

        return item_tuple_list

    except Exception as e:
        return e

