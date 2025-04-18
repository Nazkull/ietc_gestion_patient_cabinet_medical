
# 🏥 Projet de Gestion de Cabinet Médical

Ce projet simule la gestion d’un cabinet médical. Il permet la prise de rendez-vous en ligne, la gestion de dossiers médicaux, l’envoi de rappels automatiques, et la consultation des prescriptions. Le tout repose sur une structure orientée objet en Python 3.1.

---

## ✅ Fonctionnalités principales

### 1. 🧑‍⚕️ Gestion des entités

- **Classe `Patient`**
  - Nom, prénom, date de naissance
  - Adresse, téléphone, email
  - Numéro de sécurité sociale
  - Liste des allergies
  - Liste des antécédents médicaux

- **Classe `Medecin`**
  - Nom, prénom, spécialité
  - Numéro RPPS
  - Adresse du cabinet, téléphone, email

- **Classe `RendezVous`**
  - Identifiant
  - Date et heure du rendez-vous
  - Lien avec un `Patient` et un `Medecin`
  - Motif du rendez-vous
  - Statut (`Planifie`, `Confirme`, `Annule`, `Effectue`)

- **Classe `DossierMedical`**
  - ID du dossier
  - Date de création
  - Liste des consultations passées (`Consultation`)
  - Liste des traitements en cours (`Traitement`, à définir)

- **Classe `Consultation`**
  - ID de la consultation
  - Date et heure
  - Motif, diagnostic, notes
  - Lien vers une prescription (`Prescription`)
  - Médecin responsable

- **Classe `Prescription`**
  - ID de l’ordonnance
  - Date de prescription
  - Posologie et instructions
  - Médicaments associés (liste de `Medicament`)
  - Patient et médecin liés à la prescription

- **Classe `Medicament`**
  - Nom commercial et générique
  - Dosage
  - Forme (comprimé, sirop, etc.)

- **Classe `RappelAutomatique`**
  - ID du rappel
  - Type de rappel (`Email`, `SMS`)
  - Date d’envoi
  - Statut (`Planifie`, `Envoye`, `Erreur`)
  - Lié à un `RendezVous`

---

### 2. 📅 Prise de rendez-vous en ligne

- Choix du médecin, de la date et de l’heure
- Affichage des créneaux disponibles
- Enregistrement dans une instance `RendezVous`

---

### 3. 🔔 Système de rappel automatique

- Classe `RappelAutomatique` pour chaque `RendezVous`
- Rappel envoyé par :
  - Email (via `smtplib`)
  - SMS (via API type Twilio)
- Suivi de l’état du rappel (planifié, envoyé, erreur)

---

### 4. 📂 Gestion des dossiers médicaux

- Chaque patient a un `DossierMedical` unique
- Possibilité d’ajouter des `Consultation`
- Visualisation des traitements en cours
- Archivage sécurisé (format `.json` ou autre)

---

### 5. 💊 Gestion des prescriptions

- Ajout de `Prescription` via une `Consultation`
- Association de plusieurs `Medicament`
- Informations sur la posologie et les instructions
- Éventuel export en PDF (optionnel)

---

### 6. 🖥️ Interface graphique

- Application desktop (Tkinter / CustomTkinter)
- Navigation fluide entre :
  - Liste des patients
  - Calendrier des rendez-vous
  - Fiches médecin et dossier médical
- UI moderne et ergonomique

---

## 💡 Technologies utilisées

| Élément | Détail |
|--------|--------|
| **Langage** | Python 3.x |
| **POO** | Oui, chaque entité est une classe |
| **Interface** | Tkinter ou CustomTkinter |
| **Base de données** | `.json` local |
| **Emails** | SMTP via `smtplib` |
| **SMS** | API Twilio ou équivalent |
| **Organisation** | Fichiers séparés : `patient.py`, `medecin.py`, `rendezvous.py`, etc. |
