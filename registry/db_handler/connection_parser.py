import os

from urllib.parse import urlparse

def parse_mssql_connection(connection_str):
    parts = dict([p.strip().split("=", 1) for p in connection_str.split(";") if len(p.strip()) > 0])
    server = parts["Server"].split(":")[1].split(",")[0]
    return {
        "host": server,
        "database": parts["Initial Catalog"],
        "user": parts["User ID"],
        "password": parts["Password"],
        # "charset": "utf-8",   ## For unknown reason this causes connection failure
    }

def parse_postgres_connection(connection_str):
    parsed_url = urlparse(connection_str)
    return {
        "user": parsed_url.username,
        "password": parsed_url.password,
        "host": parsed_url.hostname,
        "port": parsed_url.port,
        "database": parsed_url.path.lstrip('/')  # Remove leading slash from path to get database name
    }