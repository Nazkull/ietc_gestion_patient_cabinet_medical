from models.staff import Staff

class Secretary(Staff):
    def __init__(self, user_id, first_name, last_name, email, phone, password, staff_id, secretary_id):
        super().__init__(user_id, first_name, last_name, email, phone, password, staff_id)
        self.secretary_id = secretary_id

    def manage_doctor_schedule(self):
        # To be implemented
        pass

    def validate_appointment(self):
        # To be implemented
        pass

    def cancel_patient_appointment(self):
        # To be implemented
        pass

    def manage_patients(self):
        # To be implemented
        pass

    def manage_billing(self):
        # To be implemented
        pass

    def __str__(self):
        return f"Secretary: {self.first_name} {self.last_name}" 