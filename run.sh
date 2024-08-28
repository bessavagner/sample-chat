#!/bin/bash

./build.sh

if [ "$PRODUCTION" -eq 1 ]; then
    echo "🐋 Running container..."
    docker run -d --name sample-chat -p 8081:8080 -v $PWD:/usr/src sample_chat:latest
else
    echo "🚧 ⚙️ Running in development mode"
    python app.py
fi
