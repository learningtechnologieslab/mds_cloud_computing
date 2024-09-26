from flask import Flask
import uuid
import json

app = Flask(__name__)


class Patient():
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.patient_id = str(uuid.uuid4())


class Visit():
    def __init__(self, patient_id, doctor_id):
        self.patient_id = patient_id
        self.doctor_id = doctor_id

class Doctor():
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.doctor_id = str(uuid.uuid4())







@app.route("/")
def index():
    patient = Patient("Dmitriy", "Babichenko")
    doctor = Doctor("Bob", "Smith")
    visit = Visit(patient.patient_id, doctor.doctor_id)

    visit_data = {
        "patient" : patient.__dict__,
        "doctor" : doctor.__dict__,
        "visit" : visit.__dict__
    }

    return json.dumps(visit_data)

app.run()

    