import requests
import time
import json
import calendar
import datetime as dt
import os
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import timedelta

# write a function to request data from the random user generator
# first check the status code
# if it is not a HTTP 200 status code then wait and retry

def fetch_random_user_data():
    # Define the directory for storing data
    data_dir = './data'
    
    # Create the data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    nameList = []
    retry_count = 0
    max_retries = 5  # Set a maximum retry limit

    while retry_count < max_retries:
        nameRequest = requests.get("https://randomuser.me/api/")
        
        if nameRequest.status_code == 200:
            for i in range(10):
                nameRequest = requests.get("https://randomuser.me/api/")
                nameList.append(nameRequest.json()['results'][0])
                time.sleep(2)

            current_GMT = time.gmtime()
            time_stamp = calendar.timegm(current_GMT)

            # Update file path to use the data directory
            FILE_PATH = os.path.join(data_dir, f'{time_stamp}.json')

            with open(FILE_PATH, 'w') as output_file:
                json.dump(nameList, output_file)

            break
        else:
            print("Retrying...")
            time.sleep(2)
            retry_count += 1
            
            
default_args = {
    'owner': 'admin',
    'start_date': dt.datetime(202, 1, 1),  # Adjust start date accordingly
    'retries': 3,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    'random_user_data_fetch',
    default_args=default_args,
    description='Fetch random user data',
    schedule_interval='* * * * *',  # Adjust as needed
    catchup=False # disable backfilling
)

fetch_data_task = PythonOperator(
    task_id='fetch_random_user_data',
    python_callable=fetch_random_user_data,
    dag=dag,
)

fetch_data_task
