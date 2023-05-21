from flask import Flask
from Scheduler import *

app = Flask(__name__)


@app.route("/")
def test():
    return "Hello, world!"