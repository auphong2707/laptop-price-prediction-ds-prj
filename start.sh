#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Start PostgreSQL service
service postgresql start

# Start the Airflow web server and scheduler
airflow webserver --port 8080 & airflow scheduler