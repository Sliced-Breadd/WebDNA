import os
from flask import Flask, request, render_template, send_file
from flask_mail import Mail, Message
import csv
from dna import *

app = Flask(__name__)

app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")

mail = Mail(app)

# List of database and sequences files
SEQUENCES = []
DATABASES = [
    "small",
    "large"
]
    
for i in range(1, 21):
    SEQUENCES.append(i)


@app.route("/")
def index():
    # Landing Page/ Route
    return render_template("index.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    # If the route is accessed with GET request form page will be displayed else result page
    if request.method == "GET":
        return render_template("profiler.html", databases=DATABASES, sequences=SEQUENCES)
    else:
        sequence_file = "static/sequences/" + request.form.get("sequence_file") + ".txt"
        database_file = "static/databases/" + request.form.get("database_file") + ".csv"

        # Main DNA profiler function called from dna.py
        dna_profile_res = dna_main(database_file, sequence_file)
        
        # Sending email
        usr_mail = request.form.get("usr_mail")
        if not usr_mail:
            pass
        else:
            message = Message(f"Thanks for Using DNA profiler. **{dna_profile_res}** was found in the sequence you selected", recipients=[usr_mail])
            mail.send(message)

        return render_template("success.html", message=dna_profile_res)

@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "GET":
        return render_template("about.html", sequences=SEQUENCES)


@app.route("/database/<db_selected>", methods=["GET", "POST"])
def dblarge(db_selected):
    if db_selected == "large":
        return render_template("largecsv.html", db_file="Large")
    else:
        return render_template("smallcsv.html", db_file="Small")

@app.route("/sequence", methods=["POST"])
def sequence():
    seq_file = request.form.get("sequence_file")
    return send_file(f"sequences/{seq_file}.txt")

@app.route("/test")
def test():
    return render_template("error.html")