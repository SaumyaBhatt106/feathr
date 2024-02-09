import os
import pymssql
import sqlite3
import logging
import psycopg2
import threading

from typing import List, Dict
from .connection_parser import parse_mssql_connection, parse_postgres_connection
from .utils import flatten_tuple
from .db_connection_interface import DbConnection
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

import platform
if platform.system().lower().startswith('dar'):
    import _scproxy

psycopg2.extras.register_uuid()
REGISTRY_DB_URL = os.environ["CONNECTION_STR"]

class SQLiteConnection(DbConnection):

    def __init__(self):
        # use ` check_same_thread=False` otherwise an error like 
        # sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread. The object was created in thread id 140309046605632 and this is thread id 140308968896064.
        # will be thrown out
        # Use the mem just to make sure it can connect. The actual file path will be initialized in the db_registry.py file
        self.mutex = threading.Lock()
        self.conn = sqlite3.connect("file::memory:?cache=shared", uri=True, check_same_thread=False)
        self._is_sqlalchemy_supported = True

    def connect(autocommit = True):
        # This is just to implement the abstract method. It's usually not used.
        return SQLiteConnection()

    def query(self, sql: str, *args, **kwargs) -> List[Dict]:
        # this is just to implement the abstract method.
        pass

    def update(self, sql: str, *args, **kwargs) -> List[Dict]:
        # this is just to implement the abstract method.
        pass

    @contextmanager
    def transaction(self):

        """
        Start a transaction so we can run multiple SQL in one batch.
        User should use `with` with the returned value, look into db_registry.py for more real usage.

        NOTE: `self.query` and `self.execute` will use a different MSSQL connection so any change made
        in this transaction will *not* be visible in these calls.

        The minimal implementation could look like this if the underlying engine doesn't support transaction.
        ```
        @contextmanager
        def transaction(self):
            try:
                c = self.create_or_get_connection(...)
                yield c
            finally:
                c.close(...)
        ```
        """
        conn = None
        cursor = None
        try:
            # As one MssqlConnection has only one connection, we need to create a new one to disable `autocommit`
            conn = SQLiteConnection.connect().conn
            cursor = conn.cursor()
            yield cursor
        except Exception as e:
            logging.warning(f"Exception: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.commit()

    def create_all_tables(self, file) -> None:
        conn = None
        cursor = None
        try:
            logging.info("Creating tables in SQLite")
            conn = self.conn
            cursor = self.conn.cursor()
            yield cursor
        except Exception as e:
            logging.warning(f"Exception: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                try:
                    with open(file, 'r') as f:
                        sql_statements = f.read()
                        cursor.executescript(sql_statements)
                    conn.commit()
                    logging.info("Created tables successfully")
                except Exception as e:
                    logging.warning(f"Exception: {e}")
                    conn.rollback()
                    raise e


class MssqlConnection(DbConnection):

    def __init__(self, params):
        self.params = params
        self.conn = pymssql.connect(**self.params)
        self.mutex = threading.Lock()
        self._is_sqlalchemy_supported = False

    def connect(autocommit = True):
        params = parse_mssql_connection(REGISTRY_DB_URL)
        if not autocommit:
            params["autocommit"] = False
        return MssqlConnection(params)

    def query(self, sql: str, *args, **kwargs) -> List[Dict]:
        """
        Make SQL query and return result
        """
        logging.debug(f"SQL: `{sql}`")
        while True:
            try:
                with self.mutex:
                    c = self.conn.cursor(as_dict=True)
                    c.execute(sql, *args, **kwargs)
                    return c.fetchall()
            except pymssql.OperationalError as e:
                logging.warning(f"Database error --- {e}")
                pass

    def update(self, sql: str, *args, **kwargs):
        try:
            with self.mutex:
                c = self.conn.cursor(as_dict=True)
                c.execute(sql, *args, **kwargs)
                self.conn.commit()
                return True
        except pymssql.OperationalError as e:
            logging.warning(f"Database error --- {e}")

    @contextmanager
    def transaction(self):
        """
        Start a transaction so we can run multiple SQL in one batch.
        User should use `with` with the returned value, look into db_registry.py for more real usage.

        NOTE: `self.query` and `self.execute` will use a different MSSQL connection so any change made
        in this transaction will *not* be visible in these calls.

        The minimal implementation could look like this if the underlying engine doesn't support transaction.
        ```
        @contextmanager
        def transaction(self):
            try:
                c = self.create_or_get_connection(...)
                yield c
            finally:
                c.close(...)
        ```
        """
        conn = None
        cursor = None
        try:
            # As one MssqlConnection has only one connection, we need to create a new one to disable `autocommit`
            conn = MssqlConnection.connect(autocommit=False).conn
            cursor = conn.cursor(as_dict=True)
            yield cursor
        except Exception as e:
            logging.warning(f"Exception: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.commit()

    def create_all_tables(self, file) -> None:
        try:
            conn = self.conn
            cursor = conn.cursor()
            with open(file, 'r') as f:
                sql_statements = f.read()
                cursor.execute(sql_statements)
            conn.commit()
            print("Tables created successfully in MSSQL")
        except pymssql.Error as e:
            print("Error creating tables in MSSQL:", e)


class PostgresConnection(DbConnection):

    def __init__(self, params):
        self.params = params
        self.conn = psycopg2.connect(**self.params)
        self.mutex = threading.Lock()
        self._is_sqlalchemy_supported = True

    def connect(autocommit=True):
        params = parse_postgres_connection(REGISTRY_DB_URL)
        if not autocommit:
            params["autocommit"] = False
        return PostgresConnection(params)

    def query(self, sql: str, *args, **kwargs) -> List[Dict]:
        """
        Make SQL query and return result
        """
        logging.debug(f"SQL: `{sql}`")
        try:
            with self.mutex:
                c = self.conn.cursor(cursor_factory=RealDictCursor)
                c.execute(sql, flatten_tuple(args), **kwargs)
                return c.fetchall()
        except psycopg2.OperationalError as e:
            logging.error(f"Database error --- {e}")

    def update(self, sql: str, *args, **kwargs) -> List[Dict]:
        logging.debug(f"SQL: `{sql}`")
        try:
            with self.mutex:
                c = self.conn.cursor(cursor_factory=RealDictCursor)
                c.execute(sql, flatten_tuple(args), **kwargs)
                self.conn.commit()
        except psycopg2.OperationalError as e:
            logging.error(f"Database error --- {e}")

    @contextmanager
    def transaction(self):
        """
        Start a transaction for running multiple SQL queries in one batch.t
        """
        conn = None
        cursor = None
        try:
            conn = self.conn
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            yield cursor
        except Exception as e:
            logging.error(f"Exception: {e}")
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.commit()

    def create_all_tables(self, file) -> None:
        try:
            conn = self.conn
            cursor = conn.cursor()
            with open(file, 'r') as f:
                sql_statements = f.read()
                cursor.execute(sql_statements)
            conn.commit()
            logging.info("Tables created successfully in PostgreSQL")
        except psycopg2.Error as e:
            logging.error("Error creating tables in PostgreSQL:", e)
        finally:
            if cursor:
                cursor.close()

