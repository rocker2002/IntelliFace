# Use Python 3.10 slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create staticfiles directory
RUN mkdir -p staticfiles

# Expose port
EXPOSE $PORT

# Create startup script
RUN echo '#!/bin/bash\n\
echo "🚀 Starting IntelliFace..."\n\
echo "📊 Collecting static files..."\n\
python manage.py collectstatic --noinput\n\
echo "🗄️ Running migrations..."\n\
python manage.py migrate --noinput || echo "⚠️ Migration failed, continuing..."\n\
echo "🌐 Starting Gunicorn..."\n\
exec gunicorn IntelliFace.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120\n' > /app/start.sh && chmod +x /app/start.sh

# Run the application
CMD ["/app/start.sh"]