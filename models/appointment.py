from datetime import datetime

class Appointment:
    def __init__(self, appointment_id, patient_id, doctor_id, start_time, end_time, reason, status="planned", appt_type="first"):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.start_time = start_time
        self.end_time = end_time
        self.reason = reason
        self.status = status  # planned, confirmed, cancelled, completed
        self.appointment_type = appt_type # first, follow-up, urgent

    def create(self):
        # à implémenter plus tard
        pass

    def confirm(self):
        self.status = "confirmed"
        # à implémenter plus tard
        pass

    def modify(self, new_start_time=None, new_end_time=None):
        if new_start_time:
            self.start_time = new_start_time
        if new_end_time:
            self.end_time = new_end_time
        # à implémenter plus tard
        pass

    def cancel(self):
        self.status = "cancelled"
        # à implémenter plus tard
        pass

    def __str__(self):
        return f"RDV ID: {self.appointment_id} le {self.start_time.strftime('%Y-%m-%d %H:%M')} avec Dr. [Nom du Dr]" 