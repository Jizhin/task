# Use official Python image
FROM python:3.11-slim

# Set environment vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

RUN python manage.py collectstatic --noinput
# Run server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8003", "talks_project.asgi:application"]