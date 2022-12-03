import requests
import random
import time
import json


#thingsboard_host = ["localhost:9090", "10.147.17.212:9090"]
thingsboard_host = ["localhost:9999"]

t1_access_token = "5NrIUqk7m2yAFaSbnL93"
th1_access_token = "KQJpWxMOkrQZIWHFzUwC"

temperatures = [20, 21, 23.5, 26.1, 20.7, 22, 22.11]
humidities = [20, 34, 23, 53, 54, 67, 73, 84, 91]
battery_levels = [10, 39, 65, 90]

headers =  { 
            "Content-Type" : "application/json"
            }


while True:
    # send temperature data
    data = {
        "timestamp" : time.time(),
        # "device_id" : f"tmp00{i}",
        "temperature" : random.choice(temperatures),
    }

    for host in thingsboard_host:
        url = f"http://{host}/api/v1/{t1_access_token}/telemetry"
        requests.post(url, json.dumps(data), headers=headers)
    
    # send TH data
    data = data = {
        "timestamp" : time.time(),
        # "device_id" : f"tmp00{i}",
        "temperature" : random.choice(temperatures),
        "humidity": random.choice(humidities)
    }

    for host in thingsboard_host:
        url = f"http://{host}/api/v1/{th1_access_token}/telemetry"
        requests.post(url, json.dumps(data), headers=headers)
    
    time.sleep(60)
