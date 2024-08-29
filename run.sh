#!/bin/bash

if [ "$PRODUCTION" -eq 1 ]; then
    echo "🐋 Running container..."
    docker run -d --name sample-chat -p 8081:8080 sample_chat:latest
else
    echo "🚧 ⚙️ Running in development mode"
    echo "run 'npx tailwindcss -i ./static/css/input.css -o ./static/css/styles.css --watch' to apply your changes on input.css while devloping"
    python app.py
fi
