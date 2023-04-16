import json
import requests
from flask import Flask, render_template, request, flash, jsonify
app = Flask(__name__, static_folder='static')
app.secret_key = "chatgpt"

# from sele import *

@app.route('/data')
def get_data():
    with open('test.json', 'rb') as f:
        data = json.load(f)
    return jsonify(data)


@app.route('/')
def index():
    # Read the JSON data from a file
    
    # print(data)
    # Render the index.html template, passing in the JSON data as a variable
    # saveData("test.json", runProgram(urlList, tagNameList))
    return render_template('layout.html')


# @app.route("/", methods=['POST', 'GET'])
# def index():
#     # if request.method == 'POST':
#     #     input_text = request.form['input_text']
#     #     output_text = main(input_text) # process_text is a function that returns the answer of the chatbot
#     #     return jsonify({'output_text': output_text})
#     return render_template('layout.html')

# response = requests.get('http://localhost:5000/data')
# data = response.json()