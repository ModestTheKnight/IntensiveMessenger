from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, Intensive Messenger!"

@app.route("/status")
def status():
    return jsonify({
        'status':'OK',
        'name':'Intensive Messenger',
        'time': datetime.now()
    })

app.run()