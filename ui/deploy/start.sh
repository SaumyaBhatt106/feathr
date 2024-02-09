#!/bin/bash

# Generate static env.config.js for UI app
envfile=/usr/share/nginx/html/env-config.js

if [[ -z "${REACT_APP_ENABLE_RBAC}" ]]; then
    echo "Environment variable REACT_APP_ENABLE_RBAC is not defined, skipping"
else
    echo "  \"enableRBAC\": \"${REACT_APP_ENABLE_RBAC}\"," >> $envfile
fi

echo "Successfully generated ${envfile} with following content"
cat $envfile

# Start nginx
nginx
