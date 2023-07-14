#!/bin/bash

if [[ -z "${DEV}" ]]; then
    echo "Running in production mode"
    uvicorn --factory proqa_ai.server:create_app --host $SERVER_HOST --port $SERVER_PORT
else
    echo "Running in development mode"
    uvicorn --factory proqa_ai.server:create_app --host $SERVER_HOST --port $SERVER_PORT --reload
fi