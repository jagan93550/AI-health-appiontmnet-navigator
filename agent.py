from tools import find_nearby_hospitals
from models import Doctor

SYMPTOM_MAP = {
    "chest pain": "Cardiology",
    "heart pain": "Cardiology",

    "fever": "General Physician",
    "cold": "General Physician",
    "cough": "General Physician",
    "body pain": "General Physician",

    "headache": "Neurology",
    "migraine": "Neurology",
    "dizziness": "Neurology",

    "stomach pain": "Gastroenterology",
    "vomiting": "Gastroenterology",

    "skin rash": "Dermatology",
    "itching": "Dermatology"
}

class HealthAgent:
    def __init__(self, db):
        self.db = db

    def run(self, symptoms, city):
        
        specialty = "General Physician"
        symptoms_text = symptoms.lower()

        for symptom, spec in SYMPTOM_MAP.items():
            if symptom in symptoms_text:
                specialty = spec
                break   # stop after first match

        # Find nearby hospitals (API)
        hospitals = find_nearby_hospitals(city)

        #  Find doctor from database
        doctor = self.db.query(Doctor).filter(
            Doctor.specialty == specialty
        ).first()

        #   Safe doctor check
        if doctor:
            doctor_name = doctor.doctor_name
            time = doctor.available_time
        else:
            doctor_name = "No doctor available"
            time = "N/A"

        # 🔹 Final response
        return {
             "specialty": specialty,
              "hospital": hospitals[0] if hospitals else "Not Found",
              "doctor": doctor_name,
               "time": time
        }

