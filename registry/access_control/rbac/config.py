import os

# API Settings
# RBAC_API_BASE: str = _get_config("RBAC_API_BASE")

# Authentication
RBAC_API_CLIENT_ID: str = os.environ.get("RBAC_API_CLIENT_ID", "")
RBAC_AAD_TENANT_ID: str = os.environ.get("RBAC_AAD_TENANT_ID", "")
RBAC_AAD_INSTANCE: str = os.environ.get("RBAC_AAD_INSTANCE", "")
RBAC_API_AUDIENCE: str = os.environ.get("RBAC_API_AUDIENCE", "")

# SQL Database
RBAC_CONNECTION_STR: str = os.environ.get("RBAC_CONNECTION_STR")

# Downstream API Endpoint
RBAC_REGISTRY_URL: str = os.environ.get("RBAC_REGISTRY_URL")

DUMMY_AUTH: str = os.environ.get("DUMMY_AUTH")
