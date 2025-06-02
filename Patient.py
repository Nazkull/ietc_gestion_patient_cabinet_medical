class Patient:
    def __init__(self, first_name, last_name, age, patient_id, phone_number, email):
        #constructeur patient
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.patient_id = patient_id
        self.phone_number = phone_number
        self.email = email
#fonction pour afficher les infos du patient
    def show_info(self):
        return f"Patient ID: {self.patient_id}\nName: {self.first_name} {self.last_name}\nAge: {self.age} years old\nPhone: {self.phone_number}\nEmail: {self.email}"



