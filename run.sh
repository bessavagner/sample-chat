#!/bin/bash

if [ "$PRODUCTION" -eq 1 ]; then
    echo "🐋 Running container..."
    npm run build
    docker run -d --name sample-chat -p 8081:8080 sample_chat:latest
else
    echo "🚧 ⚙️ Running in development mode"
    python app.py
fi
