from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!"


@app.route('/api/intake')
def intake():
    return "Hello World!"


@app.route('/api/v1/series')
def series():
    return "Hello World!"
