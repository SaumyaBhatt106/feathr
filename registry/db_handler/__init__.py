import os

from .enums import Provider
from .connection_providers import SQLiteConnection, MssqlConnection, PostgresConnection

def provide_db_connection(provider_env):
    match provider_env:

        case Provider.SQLITE.value:
            return SQLiteConnection
        
        case Provider.MSSQL.value:
            return MssqlConnection
        
        case Provider.POSTGRESQL.value:
            return PostgresConnection
        
        case _:
            return provide_default_connection()
        
def provide_default_connection():
    return SQLiteConnection