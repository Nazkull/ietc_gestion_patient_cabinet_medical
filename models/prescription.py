from datetime import datetime
import uuid

class Prescription:
    def __init__(self, patient_id, doctor_id, medications=None, instructions="", prescription_id=None):
        self.prescription_id = prescription_id or f"PR-{str(uuid.uuid4())[:8].upper()}"
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = datetime.now().isoformat()
        self.medications = medications or []
        self.instructions = instructions
    
    def to_dict(self):
        return {
            'prescription_id': self.prescription_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'date': self.date,
            'medications': self.medications,
            'instructions': self.instructions
        }
    
    @classmethod
    def from_dict(cls, data):
        prescription = cls(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            medications=data.get('medications', []),
            instructions=data.get('instructions', ''),
            prescription_id=data['prescription_id']
        )
        prescription.date = data['date']
        return prescription
    
    def add_medication(self, name, dosage, frequency, duration, notes=""):
        """Ajoute un médicament à l'ordonnance."""
        medication = {
            'name': name,
            'dosage': dosage,
            'frequency': frequency,
            'duration': duration,
            'notes': notes
        }
        self.medications.append(medication)
    
    def remove_medication(self, index):
        """Supprime un médicament de l'ordonnance."""
        if 0 <= index < len(self.medications):
            del self.medications[index]
    
    def get_formatted_date(self):
        """Retourne la date formatée."""
        return datetime.fromisoformat(self.date).strftime('%d/%m/%Y')

    def __str__(self):
        return f"Prescription ID: {self.prescription_id} from {self.date[:10]}" 