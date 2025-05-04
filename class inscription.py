class Inscription:
    def __init__(self, name, firstname, birthdate, email, password):
        self.name = name
        self.firstname = firstname
        self.birthdate = birthdate
        self.email = email
        self.password = password

    def enregistrer_dans_fichier(self):
        # Créer une ligne avec toutes les informations séparées par des points-virgules
        ligne = f"{self.name};{self.firstname};{self.birthdate};{self.email};{self.password}\n"

        try:
            # Ouvrir le fichier en mode append (a) pour ajouter à la fin du fichier
            with open("inscriptions.txt", "a") as fichier:
                fichier.write(ligne)
            return True
        except Exception as e:
            print(f"Erreur lors de l'enregistrement : {e}")
            return False


# Programme principal
def main():
    # Demander les informations à l'utilisateur
    nom = input("Entrez votre nom : ")
    prenom = input("Entrez votre prénom : ")
    date_naissance = input("Entrez votre date de naissance (JJ/MM/AAAA) : ")
    email = input("Entrez votre email : ")
    mot_de_passe = input("Entrez votre mot de passe : ")

    # Créer une instance de la classe Inscription
    utilisateur = Inscription(nom, prenom, date_naissance, email, mot_de_passe)

    # Enregistrer dans le fichier
    if utilisateur.enregistrer_dans_fichier():
        print("\nInscription enregistrée avec succès !")
        print("\nInformations enregistrées :")
        print(f"Nom : {utilisateur.name}")
        print(f"Prénom : {utilisateur.firstname}")
        print(f"Date de naissance : {utilisateur.birthdate}")
        print(f"Email : {utilisateur.email}")
        print(f"Mot de passe : {'*' * len(utilisateur.password)}")
    else:
        print("Erreur lors de l'enregistrement de l'inscription.")


if __name__ == "__main__":
    main()