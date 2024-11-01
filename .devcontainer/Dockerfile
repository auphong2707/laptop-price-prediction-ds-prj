# Base image
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV AIRFLOW_HOME=/app/airflow

# [PYTHON]
# Copy requirements and install dependencies
COPY requirements.txt .

# Install Airflow
RUN pip install --no-cache-dir apache-airflow==2.10.2 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.10.2/constraints-3.11.txt"

# Install Python packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# [APT]
# Update package list
RUN apt-get update

# Install Firefox
RUN apt-get install -y --no-install-recommends firefox-esr

# Install PostgreSQL
RUN apt-get install -y --no-install-recommends postgresql postgresql-contrib

# Install sudo
RUN apt install -y sudo

# Set up PostgreSQL database and user
USER postgres

# Start PostgreSQL, create database and user, then stop PostgreSQL
RUN service postgresql start && \
    psql -c "CREATE USER airflow PASSWORD 'airflow';" && \
    psql -c "CREATE DATABASE airflow;" && \
    psql -c "GRANT ALL PRIVILEGES ON DATABASE airflow TO airflow;" && \
    psql -d airflow -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO airflow;" && \
    psql -d airflow -c "GRANT USAGE ON SCHEMA public TO airflow;" && \
    psql -d airflow -c "GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO airflow;" && \
    psql -c "ALTER DATABASE airflow OWNER TO airflow;" && \
    service postgresql stop

# Switch back to root user
USER root