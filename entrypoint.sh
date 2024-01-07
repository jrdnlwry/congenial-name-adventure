#!/bin/bash

# Initialize the Airflow database
airflow db init

# Create an admin user (change these details as needed)
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Start the Airflow webserver
## exec airflow webserver

# Hand off to the CMD (webserver & scheduler hopefully)
exec "$@"
