import requests
import time
import pprint
from datetime import datetime, timedelta
from collections import defaultdict
from threading import Thread, Lock

from database import DatabaseAccess


AGGREGATION_INTERVAL_S = 5 * 60 # has to be less than an hour and multiple of a minute. should cleanly divide the hour, otherwise there will be a shorter gap between two hours
# AGGREGATION_TIME_S = 5 * 4
POLL_INTERVAL_S = 5

base = "http://192.168.1.237/solar_api/v1/" 
power_uri = base + "GetPowerFlowRealtimeData.fcgi"
battery_uri = base + "GetStorageRealtimeData.cgi"

values = defaultdict(list)
lock = Lock()

def aggregate(dictionary: defaultdict) -> dict:
    return {key: sum(value)/len(value) for key, value in dictionary.items()}

def call_api(values: defaultdict, lock: Lock):
    power_response = requests.get(power_uri)
    power_values = power_response.json()['Body']['Data']['Site']
    battery_response = requests.get(battery_uri)

    with lock:
        values["p_akku"].append(power_values["P_Akku"])
        values["p_grid"].append(power_values["P_Grid"])
        values["p_load"].append(power_values["P_Load"])
        values["p_pv"].append(power_values["P_PV"])
        values["relative_charge"].append(battery_response.json()['Body']['Data']['0']['Controller']['StateOfCharge_Relative'])

def compute_next_aggregation_time_s():
    current_time = time.monotonic()
    now = datetime.now()
    time_to_next_aggregation_s = AGGREGATION_INTERVAL_S - (((now.minute * 60 + now.second) + now.microsecond / 1_000_000) % AGGREGATION_INTERVAL_S)
    # print("time to next aggregation: ", time_to_next_aggregation_s)
    return current_time + time_to_next_aggregation_s

def polling_loop(lock):
    next_poll = time.monotonic()
    
    while True:
        global values
        with lock:
            target_values = values # save reference to value in case the new dictionary is introduce during the request
        next_poll += POLL_INTERVAL_S
        Thread(target=call_api, args=(target_values, lock)).start()
        time.sleep(max(0, next_poll - time.monotonic()))

def aggregation_loop():
    global values
    db = DatabaseAccess()

    while True:
        next_aggregation_s = compute_next_aggregation_time_s()
        time.sleep(max(0, next_aggregation_s - time.monotonic()))

        with lock:
            old_values = values
            values = defaultdict(list)
        

        # round to full minutes
        timestamp = datetime.now()
        timestamp = timestamp - timedelta(minutes=timestamp.minute % (AGGREGATION_INTERVAL_S // 60), seconds=timestamp.second, microseconds=timestamp.microsecond)
        time.sleep(min(POLL_INTERVAL_S * 2, AGGREGATION_INTERVAL_S / 4)) # give inflight request some more time, number here are arbitrary

        aggregated_values = aggregate(old_values)
        aggregated_values['time'] = timestamp
        pprint.pprint(aggregated_values)
        Thread(target=db.insert, args=(aggregated_values, )).start()

if __name__ == '__main__':
    poller = Thread(target=polling_loop, args=(lock, ), daemon=True)
    aggregator = Thread(target=aggregation_loop, daemon=True)

    poller.start()
    aggregator.start()

    poller.join()
    aggregator.join()








