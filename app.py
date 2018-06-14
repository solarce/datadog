from flask import Flask, request
from storage import wavefront

app = Flask(__name__)

@app.route('/')
def index():
  return "Hello DataDog!\n"

@app.route('/metricsvc/api/v1/series', methods=['POST', 'GET'])
def series():
  if request.method == 'POST':
    wavefront.process_request(request)
  return "success"

# dd-agent posts to /metricsvc/api/v1/series/
@app.route('/metricsvc/api/v1/series/', methods=['POST', 'GET'])
def series_slash():
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