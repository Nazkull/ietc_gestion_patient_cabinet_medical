# Centre Médical Coruscant – Application de Gestion de Patients & Rendez-vous

Bienvenue ! Cette application Python permet au personnel médical (patients, médecins et secrétaires) de gérer facilement les rendez-vous et dossiers patients à l’aide d’une interface graphique moderne basée sur Tkinter.

> 🔰 Objectif de ce guide : permettre à **toute personne** de cloner le projet, d’installer les dépendances puis de démarrer l’application sans effort.

---

## 📁 Structure du dépôt

```
├── assets/           # Images et ressources graphiques
├── data/             # Fichiers JSON persistants (utilisateurs, RDV, …)
├── gui/              # Composants de l’interface graphique
├── managers/         # Logique métier (utilisateurs, planning, rappels…)
├── models/           # Modèles de données (Patient, Médecin, etc.)
├── main.py           # Point d’entrée principal (lance l’UI)
├── config.py         # Paramètres globaux de l’application
├── requirements.txt  # Dépendances Python
└── README.md         # Ce document
```

---

## 🚦 Prérequis

1. **Python ≥ 3.9** (Tkinter inclus)
2. (Optionnel mais recommandé) **Environnement virtuel** :
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```


---

## 📦 Installation des dépendances

Toutes les librairies Python nécessaires se trouvent dans `requirements.txt` ; installez-les d’un coup :

```bash
pip install -r requirements.txt
```

Détail des principales dépendances :

| Package | Version | Rôle dans le projet |
|---------|---------|---------------------|
| babel | 2.17.0 | Formatage/l10n des dates et heures |
| customtkinter | 5.2.2 | Widgets Tkinter modernes (look & feel) |
| darkdetect | 0.8.0 | Détection automatique du thème OS (clair/sombre) |
| packaging | 25.0 | Gestion des versions / parsing semver |
| pillow | 11.2.1 | Manipulation et affichage d’images (PNG, JPEG…) |
| schedule | 1.2.2 | Planification des tâches (rappels mails) |
| tkcalendar | 1.6.1 | Widget calendrier dans l’UI |

---

## ▶️ Lancer l’application

1. Placez-vous à la racine du projet :
   ```bash
   cd ietec_gestion_patient_cabinet_medical   # ou nom de votre dossier cloné
   ```
2. Exécutez le script principal :
   ```bash
   python main.py
   ```
3. La fenêtre « Centre Médical Coruscant » s’ouvre ; vous pouvez créer un utilisateur puis commencer à gérer vos rendez-vous !

> Remarque : les données sont stockées dans le dossier `data/` sous forme de fichiers JSON. Supprimez les fichiers pour repartir d’une base vierge.

---

## ✉️ Configuration des rappels par e-mail (optionnel)

Le système peut envoyer des rappels pour les rendez-vous du lendemain.  
Reportez-vous au fichier [`README_RAPPELS.md`](README_RAPPELS.md) pour la procédure complète (activation de l’authentification à deux facteurs Gmail, génération d’un mot de passe d’application, etc.).

---

## 🛠️ Dépannage rapide

| Problème | Solution |
|----------|----------|
| *Module introuvable* | Vérifiez que l’environnement virtuel est activé puis relancez `pip install -r requirements.txt`. |
| *La fenêtre ne s’ouvre pas* | Assurez-vous que Tkinter est installé ; il est inclus par défaut avec les distributions officielles de Python. |
| *Données corrompues* | Fermez l’application et supprimez les fichiers concernés dans `data/` (ils seront recréés). |

---

## 🤝 Contribuer

1. Forkez le dépôt et créez une branche (`git checkout -b feature/ma-feature`).
2. Commitez vos changements (`git commit -am 'Ajout ma feature'`).
3. Poussez la branche (`git push origin feature/ma-feature`).
4. Ouvrez une *pull-request*.

Merci d’avance pour votre aide !

#    Comptes 
Secretaire : secretary@clinic.com     mdp : secretary
Patient : deni@hotmail.com            mdp : deni
Docteur : david.davis@clinic.com      mdp : password

---

## 📜 Licence

Projet académique – voir le fichier `LICENSE` si présent ou contacter l’auteur principal. 