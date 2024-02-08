import os

from urllib.parse import urlparse

CONNECTION_STR = os.environ["CONNECTION_STR"]

def parse_mssql_connection():
    parts = dict([p.strip().split("=", 1) for p in CONNECTION_STR.split(";") if len(p.strip()) > 0])
    server = parts["Server"].split(":")[1].split(",")[0]
    return {
        "host": server,
        "database": parts["Initial Catalog"],
        "user": parts["User ID"],
        "password": parts["Password"],
        # "charset": "utf-8",   ## For unknown reason this causes connection failure
    }

def parse_postgres_connection():
    parsed_url = urlparse(CONNECTION_STR)
    return {
        "user": parsed_url.username,
        "password": parsed_url.password,
        "host": parsed_url.hostname,
        "port": parsed_url.port,
        "database": parsed_url.path.lstrip('/')  # Remove leading slash from path to get database name
    }