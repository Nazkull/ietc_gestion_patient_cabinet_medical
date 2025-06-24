from models.user import User

class Patient(User):
    def __init__(self, user_id, first_name, last_name, email, phone, password, patient_id, date_of_birth, social_security_number):
        super().__init__(user_id, first_name, last_name, email, phone, password)
        self.patient_id = patient_id
        self.date_of_birth = date_of_birth
        self.social_security_number = social_security_number

    def view_history(self):
        # To be implemented
        pass

    def book_appointment(self):
        # To be implemented
        pass

    def modify_appointment(self):
        # To be implemented
        pass

    def cancel_appointment(self):
        # To be implemented
        pass

    def view_invoices(self):
        # To be implemented
        pass

    def __str__(self):
        return f"Patient: {self.first_name} {self.last_name}" 