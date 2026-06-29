import requests
import time
import pprint
from collections import defaultdict
from threading import Thread, Lock


AGGREGATION_INTERVAL_S = 5 * 60
# AGGREGATION_TIME_S = 5 * 4
POLL_INTERVAL_S = 5

def aggregate(dictionary: defaultdict) -> dict:
    return {key: sum(value)/len(value) for key, value in dictionary.items()}

def call_api(values: defaultdict, lock: Lock):
    power_response = requests.get(power_uri)
    power_values = power_response.json()['Body']['Data']['Site']
    battery_response = requests.get(battery_uri)

    with lock:
        values["P_Akku"].append(power_values["P_Akku"])
        values["P_Grid"].append(power_values["P_Grid"])
        values["P_Load"].append(power_values["P_Load"])
        values["P_PV"].append(power_values["P_PV"])
        values["Relative_Charge"].append(battery_response.json()['Body']['Data']['0']['Controller']['StateOfCharge_Relative'])

base = "http://192.168.1.237/solar_api/v1/" 
power_uri = base + "GetPowerFlowRealtimeData.fcgi"
battery_uri = base + "GetStorageRealtimeData.cgi"

invoke_time = time.monotonic()
time.sleep(5 - invoke_time % 5) # sleep to the next 5 seconds
last_aggregation = invoke_time + (5 - invoke_time % 5)
values = defaultdict(list)

lock = Lock()
n = 0
while True:
    start_time = time.monotonic_ns() // 1_000_000_000
    if last_aggregation + AGGREGATION_INTERVAL_S <= start_time:
        last_aggregation = start_time
        print("Aggregation at: ", last_aggregation)
        pprint.pprint(aggregate(values))
        values = defaultdict(list)

    loop_end_time = start_time + POLL_INTERVAL_S
    Thread(target=call_api, args=(values, lock)).start()

    remainder = loop_end_time - time.monotonic()
    if remainder > 0:
        time.sleep(remainder)






