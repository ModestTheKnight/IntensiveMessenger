from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello! It's Intensive Messenger"

@app.route("/status")
def status():
    return jsonify({
        'status': True,
        'name':'Intensive Messenger',
        'time': datetime.now()
    })

app.run()