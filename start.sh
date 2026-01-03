#!/bin/bash

echo "🚀 Starting IntelliFace application..."

# Run build process
python build.py

# Start Gunicorn
echo "🌐 Starting Gunicorn server..."
exec gunicorn IntelliFace.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120