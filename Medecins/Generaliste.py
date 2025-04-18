from Medecins import Medecin


class Generaliste(Medecin):
    def __init__(self, nom: str, prenom: str, numero_inami: str):
        super().__init__(nom, prenom, "Médecin généraliste", numero_inami)
        