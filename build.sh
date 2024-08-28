#!/bin/bash
python -m pip install -r requirements.txt
npm install -D tailwindcss
npx tailwindcss -i ./src/input.css -o ./src/output.css