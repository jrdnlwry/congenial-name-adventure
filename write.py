"""
Upon execution:
    sort all json files by recency
    extract data from each file
    write to db
    delete all json files in folder
"""

import json
import os
import psycopg2
from psycopg2 import OperationalError

# for f in os.listdir("./data/"):
#     print(f)


def create_tables(db_name, db_user, db_password, db_host, db_port):
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

        # SQL for creating tables
        create_users_table = """
        CREATE TABLE IF NOT EXISTS Users (
            user_id SERIAL PRIMARY KEY,
            gender VARCHAR(10),
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            dob_age INTEGER,
            email VARCHAR(100),
            cell VARCHAR(20),
            picture_large VARCHAR(255)
        );
        """

        create_location_table = """
        CREATE TABLE IF NOT EXISTS Location (
            user_id INTEGER REFERENCES Users(user_id),
            street_number INTEGER,
            street_name VARCHAR(100),
            city VARCHAR(50),
            state VARCHAR(50),
            country VARCHAR(50),
            postcode VARCHAR(20)
        );
        """

        # Execute SQL
        cur.execute(create_users_table)
        cur.execute(create_location_table)

        # Commit and close
        conn.commit()
        cur.close()
        conn.close()
        print("Tables created successfully")

    except OperationalError as e:
        print(f"The error '{e}' occurred")


def sort_files():

    sorted_list = []

    dir_path = "./data/"

    # sort JSON files
    for file_name in sorted(os.listdir(dir_path)):
        #print(file_name)
        sorted_list.append(file_name)
        
        
    return sorted_list



def write_db(json_file):


    # database connection variables
    db_name = "name_db"
    db_user = "admin_user"
    db_password = "admin_password"
    db_host = "localhost"
    db_port = "5432"
    # open the database connection
    conn = psycopg2.connect(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
    )
    cur = conn.cursor()

    with open(f'./data/{json_file}') as name_file:
        file_contents = name_file.read()

    # print(file_contents)
    parsed_json = json.loads(file_contents)
    #print(parsed_json)
    for elem in parsed_json:
        # TESTING PURPOSES
        # print(elem['gender'])
        # print(elem['name']['first'])
        # print(elem['name']['last'])

        # print(elem['location']['street']['number'])
        # print(elem['location']['street']['name'])
        # print(elem['location']['city'])
        # print(elem['location']['state'])
        # print(elem['location']['country'])
        # print(elem['location']['postcode'])
        # print(elem['dob']['age'])
        # print(elem['email'])
        # print(elem['cell'])
        # print(elem['picture']['large'])
        # print()

        gender= elem['gender']
        Fname= elem['name']['first']
        Lname= elem['name']['last']

        street_num = elem['location']['street']['number']
        street_name = elem['location']['street']['name']
        city = elem['location']['city']
        state = elem['location']['state']
        country = elem['location']['country']
        zip = elem['location']['postcode']
        age = elem['dob']['age']
        email = elem['email']
        mobile_ph = elem['cell']
        picture = elem['picture']['large']
        
        # Insert user and get user_id
        cur.execute("INSERT INTO users (gender, first_name, last_name, dob_age, email, cell, picture_large) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING user_id", (gender, Fname, Lname, age, email, mobile_ph, picture))
        user_id = cur.fetchone()[0]
        # Insert location using the retrieved user_id
        cur.execute("INSERT INTO location (user_id, street_number, street_name, city, state, country, postcode) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, street_num, street_name, city, state, country, zip))

        # Commit the transaction
        conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()


create_tables("name_db", "admin_user", "admin_password", "localhost", "5432")

for file in sort_files():
    #print(type(file))
    write_db(file)
    # remove the file from the folder
    os.remove(f'./data/{file}')
