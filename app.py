from flask import Flask, request
from storage import influx, elasticsearch
import zlib, json, settings, time

app = Flask(__name__)

def tags_format(tags):
    new_tags={}
    for tag in tags:
        k, v = tag.split(":", 1)
        new_tags[k] = v.strip()
    return new_tags

@app.route('/')
def index():
    return "Hello DataDog!"


@app.route('/api/intake')
def intake():
    if request.method == 'POST':
        series = zlib.decompress(request.get_data())
        series = json.loads(series)
        metrics = series["metrics"]
        hostname = series["internalHostname"]
        host_tags = series["host-tags"]
        collection_timestamp = int(series["collection_timestamp"]) * 1000000000
        points = []
        for metric in metrics:
            new_tags = {"hostname": metric[3]["hostname"]}
            if "tags" in metric[3]:
                new_tags.update(tags_format(metric[3]["tags"]))
            timestamp = int(metric[1])
            value = metric[2]
            points.append(influx.play_load(metric[0], value, timestamp, new_tags))

        if "ioStats" in series:
            for drive, iostat in series["ioStats"].iteritems():
                for key, value in iostat.iteritems():
                    tags = {
                        "drive": drive
                    }
                    tags.update(host_tags)
                    points.append(influx.play_load(key.replace("%", "").replace("/", "_"), value, collection_timestamp, tags))

        if series["os"] == "linux":
            for key, metric in settings.STOCK_METRICS.iteritems():
                points.append(influx.play_load(metric.lower(), series[key], collection_timestamp, series["host-tags"]))

        for service in series["service_checks"]:
            new_tags = {"host_name": service["host_name"]}
            new_tags.update(tags_format(service["tags"]))
            points.append(influx.play_load(service["check"], service["status"], service["timestamp"], new_tags))

        influx.write_data(points)
        ext = {
            "collection_timestamp": int(series["collection_timestamp"]),
            "intake_timestamp": int(time.time()),
            "hostname": hostname
        }
        es_datas = []
        for k, events in series["events"].iteritems():
            for event in events:
                event["check"] = k
                event["type"] = "events"
                event.update(ext)
                es_datas.extend(event)

        if series["resources"]:
            resources = series["resources"]
            resources["type"] = "resources"
            resources.update(ext)
            es_datas.append(resources)

        if "processes" in series:
            for processe in series["processes"]["processes"]:
                processes = {
                    "user": processe[0],
                    "pid": processe[1],
                    "pcpu": processe[2],
                    "pmem": processe[3],
                    "vsz": processe[4],
                    "rss": processe[5],
                    "tty": processe[6],
                    "stat": processe[7],
                    "start": processe[8],
                    "time": processe[9],
                    "command": processe[10],
                    "hostname": hostname,
                    "type": "processes"
                }
                processes.update(ext)
                es_datas.append(processes)
        # TODO write es data
    return "success"


@app.route('/api/v1/series')
def series():
    if request.method == 'POST':
        series = request.get_json()
        points = []
        for serie in series["series"]:
            for point in serie["points"]:
                points.append(influx.play_load(serie["metric"], point[1], int(point[0]), {"host": serie["host"]}))
        influx.write_data(points)
    return "success"
