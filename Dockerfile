# Base image
FROM python:3.11.9-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables
ENV AIRFLOW_HOME=/app/airflow

# [PYTHON]
# Copy requirements and install dependencies
COPY . /app

# Install Python packages from requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# [APT]
# Update package list and install required packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    firefox-esr \
    postgresql \
    postgresql-contrib \
    wkhtmltopdf \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Install Geckodriver
RUN wget "https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-linux64.tar.gz" -O /tmp/geckodriver.tar.gz \
    && tar -xvzf /tmp/geckodriver.tar.gz -C /tmp/ \
    && mv /tmp/geckodriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/geckodriver \
    && rm /tmp/geckodriver.tar.gz

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

# Expose ports for PostgreSQL, Airflow and Flask
EXPOSE 5432 8080 5000

# Make sure the scripts are executable
RUN chmod +x /app/entrypoint.sh

# Run /entrypoint.sh first, then run the two scripts in parallel
CMD ["sh", "-c", "/app/entrypoint.sh"]