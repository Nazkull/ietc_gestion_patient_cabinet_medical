class Utilisateur:
    def __init__(self, id_utilisateur, nom, prenom, email, telephone, mot_de_passe):
        self.id_utilisateur = id_utilisateur
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone
        self.mot_de_passe = mot_de_passe

    def s_inscrire(self):
        pass

    def se_connecter(self):
        pass

    def se_deconnecter(self):
        pass

    def envoyer_message(self):
        pass

    def lire_messages(self):
        pass

    def __str__(self):
        return f"Utilisateur: {self.prenom} {self.nom}" 