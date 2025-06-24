from models.staff import Staff

class Doctor(Staff):
    def __init__(self, user_id, first_name, last_name, email, phone, password, staff_id, doctor_id, specialty):
        super().__init__(user_id, first_name, last_name, email, phone, password, staff_id)
        self.doctor_id = doctor_id
        self.specialty = specialty

    def view_schedule(self):
        # To be implemented
        pass

    def consult_patient_file(self):
        # To be implemented
        pass

    def define_availabilities(self):
        # To be implemented
        pass

    def record_consultation(self):
        # To be implemented
        pass

    def __str__(self):
        return f"Doctor: {self.first_name} {self.last_name} ({self.specialty})" 