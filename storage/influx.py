from storage import client
import time


def write_data(data):
    json_body = [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(int(time.time()))),
            "fields": {
                "value": 0.70
            }
        }
    ]
    client.write_points(json_body)
