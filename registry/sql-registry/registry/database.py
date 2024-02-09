import os

from db_handler import provide_db_connection, provide_default_connection

SQL_ALCHEMY_SUPPORTED_FILE = "./sql-registry/scripts/sqlalchemy_schema.sql"
NON_SQL_ALCHEMY_SUPPORTED_FILE = "./sql-registry/scripts/non_sqlalchemy_schema.sql"

providers = []
env_provider = os.environ['DB_PROVIDER']

# This is ordered list. So append SQLite first
if os.environ.get("FEATHR_SANDBOX"):
    providers.append(provide_default_connection())
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
