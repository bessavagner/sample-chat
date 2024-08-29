#!/bin/bash

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi


echo "🔽 ⚙️ Installing tailwindcss"
npm install -D tailwindcss

if [ "$PRODUCTION" -eq 1 ]; then
    echo "🐋 ⚙️ Buiding docker image and styles.css for production mode"
    docker stop sample-chat
    docker rm sample-chat
    docker build -t sample_chat --rm=true .
    npx tailwindcss -i ./static/css/input.css -o ./static/css/styles.css --minify
else
    echo "🚧 ⚙️ Building assets for development mode"
    python -m pip install -r requirements.txt
    npx tailwindcss -i ./static/css/input.css -o ./static/css/styles.css
fi
