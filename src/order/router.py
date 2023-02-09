# -*- coding: UTF-8 -*-
import logging
import uuid

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
@router.get("/{order_id}")
async def get_order_by_id(order_id: str, status_code=status.HTTP_201_CREATED):
    try:
        order_tuple = order_db.get_order_by_id(order_id)

        return order_tuple

    except Exception as e:
        return e


@router.post('/')
async def add_order_and_item(order_item_body: OrderItemCreateBody):
    try:
        order = order_item_body.order
        items = order_item_body.items

        vote_tuple = (vote.name, vote.description, vote.activity_date, vote.end_time, vote.server_id)
        vote_id = order_db.insert_vote(vote_tuple)

        for option in options:
            option_tuple = (option.name, vote_id)
            await order_db.insert_option(option_tuple)

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

