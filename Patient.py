def dclass Patient:
    def __init__(self, nom, prenom, age, id_patient, telephone, email):
        # Constructeur de la classe Patient
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.id_patient = id_patient
        self.telephone = telephone
        self.email = email

    def afficher_infos(self):
        # Methode pour afficher les informations du patient
        print(f"Patient ID: {self.id_patient}")
        print(f"Nom: {self.nom}")
        print(f"Pr�nom: {self.prenom}")
        print(f"�ge: {self.age} ans")
        print(f"T�l�phone: {self.telephone}")
        print(f"Email: {self.email}")

