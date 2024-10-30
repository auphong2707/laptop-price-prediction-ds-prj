FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Airflow home
ENV AIRFLOW_HOME=/app/airflow