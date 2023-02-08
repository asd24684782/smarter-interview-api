# -*- coding: UTF-8 -*-
import logging
import uuid

from fastapi import APIRouter

from order.models import vote_db
from order.schemas import order_item_create_body

# -------------------- global -----------------------------------
router = APIRouter(
    prefix="/order",
    tags=["order"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger()

# ----------------------- api ------------------------------------
@router.get("/{order_id}")
async def get_order_by_id(order_id: str):
    try:
        votes_tuple_list = vote_db.get_server_vote(order_id)

        return votes_tuple_list

    except Exception as e:
        return e


@router.post('/')
async def add_order_and_item(order_item_body: order_item_create_body):
    try:
        vote = vote_body.vote
        options = vote_body.vote_options

        vote_tuple = (vote.name, vote.description, vote.activity_date, vote.end_time, vote.server_id)
        vote_id = await vote_db.insert_vote(vote_tuple)

        for option in options:
            option_tuple = (option.name, vote_id)
            await vote_db.insert_option(option_tuple)

        return 'OK'

    except Exception as e:
        return e


@router.get('/order/{order_id}/item')
async def get_order_item(order_id: str):
    try:
        option_tuple = (option.name, option.v_id)
        await vote_db.insert_option(option_tuple)

        return 'OK'

    except Exception as e:
        return e

