import requests
import time
import json
import calendar
# write a function to request data from the random user generator
# first check the status code
# if it is not a HTTP 200 status code then wait and retry

nameList = []
nameRequest = requests.get("https://randomuser.me/api/")

while nameRequest.status_code == 200:

    for i in range(0, 10):
        nameRequest = requests.get("https://randomuser.me/api/")
        nameList.append(nameRequest.json()['results'][0])
        print("item number:", i)
        time.sleep(2)
        

    print(nameList)

    current_GMT = time.gmtime()
    time_stamp = calendar.timegm(current_GMT)

    FILE_PATH = f'./data/{time_stamp}.json'

    with open(FILE_PATH, 'w') as output_file:
        json.dump(nameList, output_file)
 
    time.sleep(2)

else:
    print("retrying...")
