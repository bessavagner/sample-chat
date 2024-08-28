#!/bin/bash

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

if [ "$PRODUCTION" -eq 1 ]; then
    echo "🐋 ⚙️ Buiding docker image for production mode"
    docker stop sample-chat
    docker rm sample-chat
    docker build -t sample_chat --rm=true .
else
    echo "🚧 ⚙️ Building assets for development mode"
    python -m pip install -r requirements.txt
    npm install
    npm run dev
fi
