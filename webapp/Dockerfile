# Use an official Python runtime as a base image
FROM python:3.12-alpine

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from writing pyc and pycache files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Copy only requirements first to leverage Docker cache
COPY app/requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container
COPY app /app

# Set the correct working directory for Django
WORKDIR /app

# Command to start Gunicorn server
CMD ["gunicorn", "webapp.wsgi:application", "--bind", "0.0.0.0:8000"]
