import logging

import psycopg2
from psycopg2.extras import execute_batch

from database import database_connection_pool

logger = logging.getLogger()

class Order:
    def __init__(self):
        self.__database_connection_pool = database_connection_pool


    def get_order_by_id(self, order_id):
        try:
            logger.info(f'get order {order_id}')
            sql = """ SELECT order_id, customer_name, custmer_id, purchase_time FROM orders WHERE order_id=%s"""
            conn = self.__database_connection_pool.connect()
            
            with conn.cursor() as cur:
                cur.execute(sql, (order_id,))
                record = cur.fetchone()

        except psycopg2.DatabaseError as e:
            logger.error(e)
            raise e

        finally:
            if conn:
                self.__database_connection_pool.disconnect(conn)
            return record


    def insert_order_and_items(self, order_insert_tuple, item_insert_tuple_list):
        logger.info("insert orders")
        try:
            # insert order
            conn = self.__database_connection_pool.connect()
            conn.autocommit = False

            insert_order_sql = """ INSERT INTO orders 
                    (order_id, customer_name, custmer_id)
                    VALUES(%s, %s, %s)
                    """

            insert_item_sql = """ INSERT INTO order_item 
                    (product_name, product_id, amount, price, order_id)
                    VALUES(%s, %s, %s, %s, %s)
                    """
  

            with conn.cursor() as cur:
                cur.execute(insert_order_sql, order_insert_tuple)
                execute_batch(cur, insert_item_sql, item_insert_tuple_list)


            conn.commit()  
            logger.info('insert successfully.')

        except psycopg2.DatabaseError as e:
            if conn:
                conn.rollback()
            logger.error(e)
            raise e

        finally:
            if conn:
                self.__database_connection_pool.disconnect(conn)
            
            return id


    def get_item_by_order_id(self, order_id):
        try:
            logger.info(f'get order {order_id} items')
            sql = """ SELECT product_name, product_id, amount, price FROM order_item WHERE order_id=%s order by id"""
            conn = self.__database_connection_pool.connect()
            
            with conn.cursor() as cur:
                cur.execute(sql, (order_id,))
                records = cur.fetchall()

        except psycopg2.DatabaseError as e:
            logger.error(e)
            raise e

        finally:
            if conn:
                self.__database_connection_pool.disconnect(conn)
            return records




order_db = Order()