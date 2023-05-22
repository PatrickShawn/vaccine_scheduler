from flask import Flask, render_template, request
from .scheduler import *

app = Flask(__name__)

username = None
date = None

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("Home.html")

@app.route("/user", methods=["GET", "POST"])
def patient_search():
    if request.method == "POST":
        global username
        username = request.form.get("username")
        password = request.form.get("password")
        patient = request.form.get("patient")
        caregiver = request.form.get("caregiver")
    if patient == "on":
        login_patient(["", username, password])
        return render_template("Patient_search.html", username=username)

@app.route("/user/search", methods=["GET", "POST"])
def patient_reserve():
    if request.method == "POST":
        global date
        global username
        date = request.form.get("patient_date")
        query_caregiver, query_vaccine = search_caregiver_schedule(["", date])
        return render_template("Patient_reserve.html", query_caregiver=query_caregiver, query_vaccine=query_vaccine, date=date, username=username)

@app.route("/user/search/reserve", methods=["GET", "POST"])
def patient_finish():
    if request.method == "POST":
        global date
        global username
        print(type(date))
        vaccine = request.form.get("patient_vaccine")
        caregiver = request.form.get("patient_caregiver")
        query_reserve = reserve(["", date, vaccine, caregiver])
        return render_template("Patient_finish.html", query_reserve=query_reserve, vaccine=vaccine, caregiver=caregiver, date=date, username=username)

