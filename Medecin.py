class Doctor:
    def __init__(self, first_name, last_name, specialty):
        self.first_name = first_name
        self.last_name = last_name
        self.specialty = specialty

    def display_info(self):
        print(f"Name: {self.first_name} {self.last_name}")
        print(f"Specialty: {self.specialty}")

class Neurologist(Doctor):
    def __init__(self, first_name, last_name, experience):
        super().__init__(first_name, last_name, "Neurology")
        self.experience = experience

    def display_info(self):
        super().display_info()
        print(f"Years of Experience: {self.experience}")

class Cardiologist(Doctor):
    def __init__(self, first_name, last_name, experience):
        super().__init__(first_name, last_name, "Cardiology")
        self.experience = experience

    def display_info(self):
        super().display_info()
        print(f"Years of Experience: {self.experience}")

class Pediatrician(Doctor):
    def __init__(self, first_name, last_name, experience):
        super().__init__(first_name, last_name, "Pediatrics")
        self.experience = experience

    def display_info(self):
        super().display_info()
        print(f"Years of Experience: {self.experience}")

class Surgeon(Doctor):
    def __init__(self, first_name, last_name, experience):
        super().__init__(first_name, last_name, "Surgery")
        self.experience = experience

    def display_info(self):
        super().display_info()
        print(f"Years of Experience: {self.experience}")

class Dermatologist(Doctor):
    def __init__(self, first_name, last_name, experience):
        super().__init__(first_name, last_name, "Dermatology")
        self.experience = experience

    def display_info(self):
        super().display_info()
        print(f"Years of Experience: {self.experience}")

class Oncologist(Doctor):
    def __init__(self, first_name, last_name, experience):
        super().__init__(first_name, last_name, "Oncology")
        self.experience = experience

    def display_info(self):
        super().display_info()
        print(f"Years of Experience: {self.experience}")

class Gynecologist(Doctor):
    def __init__(self, first_name, last_name, experience):
        super().__init__(first_name, last_name, "Gynecology")
        self.experience = experience

    def display_info(self):
        super().display_info()
        print(f"Years of Experience: {self.experience}")

class Ophthalmologist(Doctor):
    def __init__(self, first_name, last_name, experience):
        super().__init__(first_name, last_name, "Ophthalmology")
        self.experience = experience

    def display_info(self):
        super().display_info()
        print(f"Years of Experience: {self.experience}")
