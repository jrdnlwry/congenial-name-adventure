# congenial-name-adventure
This project involves a data engineering pipeline that pulls data from a random name API. The pipeline is designed to gather, process, and store data about randomly generated individuals, including their names, demographic information, and contact details. The data is structured and stored in a database for further analysis or application use.

Components
## 1. Dockerfile
Handles the environment setup, including database and table creation.
## 2. Scripts
script.py:
Gathers data from the randomized name API.
Collects data in JSON format for approximately 11 randomized people and saves it in a JSON file.
Runs indefinitely or until it encounters a non-200 status code.
Can be integrated with Apache Airflow to pause the script every hour (optional in production).
write.py:
Manages writing data to the database.
Deletes JSON files after their data is written to the respective tables.
## 3. Environment Setup
Virtual environment using Conda: conda create -n nameENV python=2.7.18.

## Proposed Architecture Diagram
![Alt text](https://github.com/jrdnlwry/data_engineering/blob/63f4cdd5fc6abcc0469ee7869c2a7fa1b67a8326/Tate%20Lowry's%20team%20library.png)
