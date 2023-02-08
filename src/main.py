# -*- coding: UTF-8 -*-
import logging
import time
from datetime import datetime

from fastapi import FastAPI

from order.router import router as order_router
#---------------- global -------------------# 
app = FastAPI()
app.include_router(order_router)

logger = logging.getLogger()
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')
#------------------- api ---------------------#
@app.on_event("startup")
async def startup_event():
    pass
        

@app.on_event("shutdown")
def shutdown_event():
    pass


@app.get('/api/1.0/ping', tags=["test"])
async def ping():
    data = {
        'message': "pong",
        'time'   : int(time.time() * 1000),
        'now'    : str(datetime.now())
    }
    return data