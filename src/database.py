import asyncio
import logging

import psycopg2
from psycopg2 import pool

from setting.setting import DB_HOST, DB_USER, DB_PASSWORD, DB_PORT, DB_NAME

logger = logging.getLogger()

class Postgres:
    """PostgreSQL Database class."""

    def __init__(self, host, user, password, port, database):
        self.__host     = host
        self.__user     = user
        self.__password = password
        self.__port     = port
        self.__database   = database
        try:
            self.__postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, 
                                                                user=self.__user,
                                                                password=self.__password,
                                                                host=self.__host,
                                                                port=self.__port,
                                                                database=self.__database)
            if (self.__postgreSQL_pool):
                logger.info("Connection pool created successfully")

        except (Exception, psycopg2.DatabaseError) as error:
            logger.info("Error while connecting to PostgreSQL", error)


    def connect(self):
        conn = None
        try:
            conn =self.__postgreSQL_pool.getconn()

        except psycopg2.DatabaseError as e:
            logger.error(e)
            raise e

        finally:
            return conn


    def disconnect(self, conn):
        logger.info('put conn')
        self.__postgreSQL_pool.putconn(conn)


database_connection_pool = Postgres(
        host=DB_HOST,
        user=DB_USER, 
        password=DB_PASSWORD,
        port=DB_PORT,
        database=DB_NAME
    )