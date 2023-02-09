# -*- coding: UTF-8 -*-
import logging
import uuid
from datetime import datetime

from fastapi import APIRouter, status, Depends


from order.dependencies import make_order_id
from order.models import order_db
from order.schemas import OrderPostSchema, OrderResponseSchema, OrderItemCreateBody, ItemResponseSchema, OrderItemResponseSchemra

# -------------------- global -----------------------------------
router = APIRouter(
    prefix="/order",
    tags=["order"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger()

# ----------------------- api ------------------------------------
@router.get("/", status_code=200)
async def get_orders():
    try:
        order_id_tuple_list = order_db.get_orders()
        logger.debug(f'order_tuple: {order_id_tuple_list}')

        return order_id_tuple_list

    except Exception as e:
        logger.error(e)
        return str(e)


@router.get("/{order_id}", response_model=OrderResponseSchema, status_code=200)
async def get_order_by_id(order_id: str):
    try:
        order_tuple = order_db.get_order_by_id(order_id)
        logger.debug(f'order_tuple: {order_tuple}')

        order = OrderResponseSchema(**{key: order_tuple[i] for i, key in enumerate(OrderResponseSchema.__fields__.keys())})

        return order

    except Exception as e:
        logger.error(e)
        return str(e)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def add_order_and_item(order_item_body: OrderItemCreateBody, order_id: str = Depends(make_order_id)):
    try:
        order = order_item_body.order
        items = order_item_body.items

        order_tuple = (order_id, order.customer_name, order.customer_id)
        logger.debug(order_tuple)

        item_tuple_list = []
        for item in items:
            item_tuple = (item.product_name, item.product_id, item.amount, item.price, order_id)
            item_tuple_list.append(item_tuple)

        logger.debug(item_tuple_list)

        order_db.insert_order_and_items(order_tuple, item_tuple_list)

        return 'OK'

    except Exception as e:
        logger.error(e)
        return str(e)


@router.put('/{order_id}', status_code=200)
async def modify_order(order_id: str, order_body: OrderPostSchema):
    try:
        order_tuple = (order_body.customer_name, order_body.customer_id, order_id)
        logger.debug(order_tuple)

        order_db.update_order(order_id, order_tuple)

        return 'OK'

    except Exception as e:
        logger.error(e)
        return str(e)


@router.get('/{order_id}/detail', response_model=OrderItemResponseSchemra, status_code=200)
async def get_order_detail(order_id: str):
    try:
        order_tuple = order_db.get_order_by_id(order_id)
        logger.debug(f'order_tuple: {order_tuple}')

        item_tuple_list = order_db.get_item_by_order_id(order_id)
        logger.debug(f'item_tuple_list: {item_tuple_list}')


        order = OrderResponseSchema(**{key: order_tuple[i] for i, key in enumerate(OrderResponseSchema.__fields__.keys())})

        items = []
        for item_tuple in item_tuple_list:
            item = ItemResponseSchema(**{key: item_tuple[i] for i, key in enumerate(ItemResponseSchema.__fields__.keys())})
            items.append(item)

        order_items = OrderItemResponseSchemra(order=order, items=items)

        return order_items

    except Exception as e:
        logger.error(e)
        return str(e)
