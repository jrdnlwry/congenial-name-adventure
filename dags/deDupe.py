import json
import os
import psycopg2
from psycopg2 import OperationalError
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import datetime as dt
from datetime import timedelta
from datetime import datetime

def clean_table_data(db_name, db_user, db_password, db_host, db_port):
    # Connection to the PostgreSQL database
    try:
        conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        cur = conn.cursor()

        # SQL for cleaning tables
        clean_user_table = """
        DELETE FROM
            users a
                USING users b
        WHERE
            a.user_id > b.user_id
            AND a.email = b.email;
        """

        clean_location_table = """
        DELETE FROM location
        WHERE user_id NOT IN (
            SELECT user_id FROM users
        );
        """
 
        # Execute SQL
        cur.execute(clean_user_table)
        cur.execute(clean_location_table)

        # Commit and close
        conn.commit()
        cur.close()
        conn.close()
        print("data cleaned successfully")

    except OperationalError as e:
        print(f"The error '{e}' occurred")



# common default arguments
default_args = {
    'owner': 'admin',
    'start_date': dt.datetime(2022, 1, 1),  # Adjust start date accordingly
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
}

# DAG for creating tables (runs once)
dedup_table_dag = DAG(
    'dedup_table_dag',
    default_args=default_args,
    description='Periodically clean the duplicate entries from both tables',
    schedule_interval=timedelta(days=1), # Adjust as needed
    catchup=False
)

table_cleansing = PythonOperator(
    task_id='clean_tables',
    python_callable=clean_table_data,
    op_kwargs={
        'db_name': "name_db",
        'db_user': "admin_user",
        'db_password': "admin_password",
        'db_host': "pg-database",
        'db_port': "5432"
    },
    dag=dedup_table_dag
)

table_cleansing