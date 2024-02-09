#!/bin/bash

LISTENING_PORT=8000

if [ "$ENABLE_RBAC" = "true" ]; then

    # Start the SQL registry server and RBAC proxy
    uvicorn sql-registry.main:app --host 0.0.0.0 --port 80 &
    uvicorn access_control.main:app --host 0.0.0.0 --port $LISTENING_PORT
else
    # Start the SQL registry server without RBAC
    uvicorn sql-registry.main:app --host 0.0.0.0 --port $LISTENING_PORT
fi
