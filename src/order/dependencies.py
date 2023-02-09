from datetime import datetime


def make_order_id():
    return datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')