#!/bin/bash

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi


echo "🔽 ⚙️ Installing tailwindcss"
npm install

if [ "$PRODUCTION" -eq 1 ]; then
    echo "🐋 ⚙️ Buiding docker image and styles.css for production mode"
    docker stop sample-chat
    docker rm sample-chat
    npm run build
    docker build -t sample_chat --rm=true .
else
    echo "🚧 ⚙️ Building assets for development mode"
    python -m pip install -r requirements.txt
    npm run dev
fi
