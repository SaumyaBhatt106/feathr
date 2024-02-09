import os

# TODO: refactor common utils in registry folder
# This is a copy of database.py from sql-registry folder 
# And add a `update` function to execute insert and set commands

from db_handler import provide_db_connection

SQL_ALCHEMY_SUPPORTED_FILE="./access_control/scripts/sqlalchemy_schema.sql"
NON_SQL_ALCHEMY_SUPPORTED_FILE="./access_control/scripts/non_sqlalchemy_schema.sql"

providers = []
env_provider = os.environ['RBAC_DB_PROVIDER']
providers.append(provide_db_connection(env_provider))

def connect(*args, **kargs):
    for p in providers:
        ret = p.connect(*args, **kargs)
        if ret is not None:
            if ret._is_sqlalchemy_supported:
                ret.create_all_tables(SQL_ALCHEMY_SUPPORTED_FILE)
            else:
                ret.create_all_tables(NON_SQL_ALCHEMY_SUPPORTED_FILE)
            return ret
    raise RuntimeError("Cannot connect to database")
