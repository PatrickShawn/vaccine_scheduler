from flask import Flask, render_template
from .scheduler import *

app = Flask(__name__)


@app.route("/")
def home():
    # return render_template("Home.html")
    login_patient(["", "Patrick", "123456"])
    search_caregiver_schedule(["", "6-3-2023"])
    return "Success"



