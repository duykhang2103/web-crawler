import json
import requests
from flask import Flask, render_template, request, flash, jsonify

from schedule import *

app = Flask(__name__, static_folder='static')
app.secret_key = "webcrawler"


@app.route('/data')
def get_data():
    data = []
    with open('static/json/tgdd-data.json', 'rb') as f:
        data1 = json.load(f)
    with open('static/json/cellphones-data.json', 'rb') as f:
        data2 = json.load(f)
    with open('static/json/gearvn-data.json', 'rb') as f:
        data3 = json.load(f)
    with open('static/json/phongvu-data.json', 'rb') as f:
        data4 = json.load(f)
    data = data + data1 + data2 + data3 + data4
    return jsonify(data)


@app.route('/')
def index():
    return render_template('layout.html')

