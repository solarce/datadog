from flask import Flask, request
from storage import wavefront
import zlib, json, settings, time

app = Flask(__name__)


def tags_format(tags):
    new_tags = {}
    if tags:
        for tag in tags:
            k, v = tag.split(":", 1)
            new_tags[k] = v.strip()
    return new_tags


@app.route('/')
def index():
    return "Hello DataDog!"

@app.route('/metricsvc/api/v1/series/', methods=['POST', 'GET'])
def series():
    if request.method == 'POST':
        wavefront.process_request(request)
    return "success"

@app.route('/metricsvc/intake/', methods=['POST', 'GET'])
def intake():
    if request.method == 'POST':
        wavefront.process_request(request)
    return "success"

@app.route('/metricsvc/api/v1/check_run/', methods=['POST', 'GET'])
def check_run():
    if request.method == 'POST':
        wavefront.process_request(request)
    return "success"