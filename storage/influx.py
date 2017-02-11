from storage import client
import time


def play_load(measurement, value, timestamp, tags):
    if value is not None:
        return {
            "measurement": measurement,
            "tags": tags,
            "time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(int(timestamp))),
            "fields": {
                "value": value
            }
        }
    else:
        return {}


def write_data(points):
    print points
    client.write_points(points)
