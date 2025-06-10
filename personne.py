import uuid

class Personne:
    """
    Représente une personne avec un ID unique, une adresse, un e-mail et un numéro de téléphone.
    """

    def __init__(self, adresse, email, telephone):
        """
        Initialise une nouvelle instance de Personne.

        Args:
            adresse (str): L'adresse de la personne.
            email (str): L'adresse e-mail de la personne.
            telephone (str): Le numéro de téléphone de la personne.
        """
        self._id = self._generer_id_unique()  # Attribut privé pour l'ID
        self.adresse = adresse
        self.email = email
        self.telephone = telephone

    def _generer_id_unique(self):
        """
        Génère un ID unique universel (UUID) pour chaque instance de Personne.
        Cet ID est garanti unique à l'échelle globale.
        """
        return str(uuid.uuid4())

    @property
    def id(self):
        """
        Propriété en lecture seule pour accéder à l'ID de la personne.
        """
        return self._id

    def __str__(self):
        """
        Retourne une représentation textuelle conviviale de l'objet Personne.
        """
        return (f"ID: {self.id}\n"
                f"Adresse: {self.adresse}\n"
                f"Email: {self.email}\n"
                f"Téléphone: {self.telephone}")

    def __repr__(self):
        """
        Retourne une représentation officielle de l'objet, utile pour le débogage.
        """
        return (f"Personne(id='{self.id}', adresse='{self.adresse}', "
                f"email='{self.email}', telephone='{self.telephone}')")