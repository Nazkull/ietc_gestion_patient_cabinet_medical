class Doctor:
    def __init__(self, first_name, last_name, specialty, inami):
        self._first_name = first_name  # Utilisation de _ pour indiquer que c'est protégé
        self._last_name = last_name
        self._specialty = specialty
        self._inami = inami

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def specialty(self):
        return self._specialty

    @property
    def inami(self):
        return self._inami

    def display_info(self):
        print(f"Name: {self.first_name} {self.last_name}")
        print(f"Specialty: {self.specialty}")
        print(f"Inami: {self.inami}")

class SpecialistDoctor(Doctor):
    def __init__(self, first_name, last_name, specialty, inami, experience):
        super().__init__(first_name, last_name, specialty, inami)
        self._experience = experience

    @property
    def experience(self):
        return self._experience

    def display_info(self):
        super().display_info()
        print(f"Years of Experience: {self.experience}")

# Création des spécialités médicales en utilisant la classe SpecialistDoctor
def create_specialist(specialty_name):
    return type(
        specialty_name,
        (SpecialistDoctor,),
        {
            '__init__': lambda self, first_name, last_name, inami, experience:
                SpecialistDoctor.__init__(self, first_name, last_name, specialty_name, inami, experience)
        }
    )

# Création des classes de spécialistes
Neurologist = create_specialist("Neurology")
Cardiologist = create_specialist("Cardiology")
Pediatrician = create_specialist("Pediatrics")
Surgeon = create_specialist("Surgery")
Dermatologist = create_specialist("Dermatology")
Oncologist = create_specialist("Oncology")
Gynecologist = create_specialist("Gynecology")
Ophthalmologist = create_specialist("Ophthalmology")