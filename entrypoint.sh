#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Start PostgreSQL service
service postgresql start

# Initialize the Airflow database without confirmation
airflow db init
airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com

# Add PostgreSQL connection to Airflow
airflow connections add 'postgres_default' \
    --conn-type 'postgres' \
    --conn-host 'localhost' \
    --conn-login 'airflow' \
    --conn-password 'airflow' \
    --conn-schema 'airflow' \
    --conn-port '5432'

# Change ownership of the start.sh file
chmod +x start.sh