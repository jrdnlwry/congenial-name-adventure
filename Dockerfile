# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Install PostgreSQL development files
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Apache Airflow (replace '2.2.0' with desired version)
RUN pip install 'apache-airflow[celery,postgres]'==2.2.0

# Copying scripts from local machine <> container
## COPY path/to/your/scripts/ /path/in/container/for/scripts/
# Copy the entire dags directory
COPY dags/ /app/dags/

# entrypoint script to copy into the container
# this script initialize the database and creates an admin user
COPY entrypoint.sh /entrypoint.sh
# this file will allow us to run webserver and scheduler within the same container
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# makes the entrypoint script executable
RUN chmod +x /entrypoint.sh


# Set an environment variable to let Airflow know where to find your DAGs
#ENV AIRFLOW__CORE__DAGS_FOLDER=/path/in/container/for/scripts/
ENV AIRFLOW__CORE__DAGS_FOLDER=/app/dags/
# typically not needed but there's additional configuration happening
ENV AIRFLOW_HOME=/usr/src/app/airflow

# Expose the port Airflow runs on
EXPOSE 8080

# Set the entrypoint script to initialize Airflow
ENTRYPOINT ["/entrypoint.sh"]

# Command to run Airflow webserver (you might want to add the scheduler as well, or use a process manager like supervisord)
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

