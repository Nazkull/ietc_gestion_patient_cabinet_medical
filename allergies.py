class Allergy:
    # Variable de classe pour stocker toutes les allergies connues
    known_allergies = []

    def __init__(self, name, severity="moderate"):
        """
        Initialise une nouvelle allergie
        :param name: Le nom de l'allergie
        :param severity: La sévérité de l'allergie (mild, moderate, severe)
        """
        self.name = name
        self.severity = severity
        self.symptoms = []
        # Ajoute l'allergie à la liste des allergies connues si elle n'existe pas déjà
        if not any(allergy.name.lower() == name.lower() for allergy in Allergy.known_allergies):
            Allergy.known_allergies.append(self)

    def add_symptom(self, symptom):
        """
        Ajoute un symptôme à la liste des symptômes
        :param symptom: Le symptôme à ajouter
        """
        if symptom not in self.symptoms:
            self.symptoms.append(symptom)

    def get_info(self):
        """
        Retourne les informations sur l'allergie
        :return: Une chaîne de caractères contenant les informations sur l'allergie
        """
        info = f"Allergy: {self.name}\n"
        info += f"Severity: {self.severity}\n"
        info += "Symptoms: " + ", ".join(self.symptoms) if self.symptoms else "No symptoms recorded"
        return info

    @classmethod
    def check_allergies(cls, items):
        """
        Vérifie si des éléments correspondent à des allergies connues
        :param items: Liste des éléments à vérifier
        :return: Liste de tuples contenant les allergies trouvées et leur sévérité
        """
        found_allergies = []
        for item in items:
            for allergy in cls.known_allergies:
                if item.lower() in allergy.name.lower():
                    found_allergies.append((allergy.name, allergy.severity))
        return found_allergies

    @classmethod
    def list_all_allergies(cls):
        """
        Liste toutes les allergies connues
        :return: Liste de toutes les allergies enregistrées
        """
        return [allergy.name for allergy in cls.known_allergies]