from flask import Flask, render_template, request
from .scheduler import *

app = Flask(__name__)

username = None
date = None

@app.route("/", methods=["GET", "POST"])
def home():
    global username
    if request.method == "POST":
        logout("")
        username = None
    return render_template("Home.html")

@app.route("/user", methods=["GET", "POST"])
def patient_search():
    global username
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        patient = request.form.get("patient")
        caregiver = request.form.get("caregiver")
        if patient == "on" and not caregiver:
            login_patient(["", username, password])
            return render_template("Patient_search.html", username=username)
        if caregiver == "on" and not patient :
            login_caregiver(["", username, password])
            return render_template("Caregiver_upload.html", username=username)
    if request.method == "GET":
        if username is not None and username_exists_patient(username):
            return render_template("Patient_search.html", username=username)
        if username is not None and username_exists_caregiver(username):
            return render_template("Caregiver_upload.html", username=username)

@app.route("/user/appointments", methods=["GET", "POST"])
def patient_appointments():
    if request.method == "POST":
        global username
        patient_query, caregiver_query,caregiver_aval = show_appointments("")
        return render_template("Patient_appointments.html", username=username, query=patient_query)

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

@app.route("/user/appointments/cancel", methods=["GET", "POST"])
def patient_cancel():
    if request.method == "POST":
       appoint_id = request.form.get("cancel")
       cancel(["", appoint_id])
       patient_query, caregiver_query,caregiver_aval = show_appointments("")
       return render_template("Patient_cancel.html", id=appoint_id, query=patient_query, username=username)

@app.route("/user/search", methods=["GET", "POST"])
def patient_reserve():
    if request.method == "POST":
        global date
        global username
        date = request.form.get("patient_date")
        query_caregiver, query_vaccine = search_caregiver_schedule(["", date])
        return render_template("Patient_reserve.html", query_caregiver=query_caregiver, query_vaccine=query_vaccine, date=date, username=username)

@app.route("/user/upload", methods=["GET", "POST"])
def caregiver_upload():
    if request.method == "POST":
        global date
        global username
        date = request.form.get("caregiver_date")
        result = upload_availability(["", date])
        return render_template("Caregiver_add.html", date=date, username=username, result=result)

@app.route("/user/upload/add_finish", methods=["GET", "POST"])
def caregiver_add():
    if request.method == "POST":
        global username
        vaccine = request.form.get("vaccine")
        doses = request.form.get("doses")
        query = add_doses(["", vaccine, doses])
        return render_template("Caregiver_finish.html", vaccine=vaccine, doses=doses, query=query, username=username, date=date)

@app.route("/user/caregiver_appointments", methods=["GET", "POST"])
def caregiver_appoints():
    if request.method == "POST":
        global username
        patient_query,caregiver_query,caregiver_aval = show_appointments("")
        return render_template("Caregiver_appointments.html", username=username, query=caregiver_query, aval=caregiver_aval)

@app.route("/user/caregiver_cancel", methods=["GET", "POST"])
def caregiver_cancel():
    if request.method == "POST":
        if request.method == "POST":
            appoint_id = request.form.get("cancel")
            cancel(["", appoint_id])
            patient_query, caregiver_query,caregiver_aval = show_appointments("")
            return render_template("Caregiver_cancel.html", id=appoint_id, query=caregiver_query, username=username)

