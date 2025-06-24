class PatientRecord:
    def __init__(self, record_id, patient_id, medical_history=""):
        self.record_id = record_id
        self.patient_id = patient_id
        self.medical_history = medical_history
        self.consultations = []
        self.prescriptions = []

    def add_consultation(self, consultation):
        self.consultations.append(consultation)

    def add_prescription(self, prescription):
        self.prescriptions.append(prescription)

    def __str__(self):
        return f"Patient Record ID: {self.record_id} for Patient ID: {self.patient_id}" 