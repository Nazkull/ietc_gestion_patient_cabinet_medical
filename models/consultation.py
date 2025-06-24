from datetime import datetime

class Consultation:
    def __init__(self, consultation_id, patient_id, doctor_id, consultation_date, reason, diagnosis, clinical_notes=""):
        self.consultation_id = consultation_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.consultation_date = consultation_date
        self.reason = reason
        self.diagnosis = diagnosis
        self.clinical_notes = clinical_notes

    def __str__(self):
        return f"Consultation ID: {self.consultation_id} on {self.consultation_date.strftime('%Y-%m-%d')}" 