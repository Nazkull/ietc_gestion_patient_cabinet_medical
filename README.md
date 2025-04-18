# 🏥 Projet de Gestion de Cabinet Médical

Ce projet a pour but de simuler la gestion d’un cabinet médical, avec la possibilité pour les patients de prendre rendez-vous en ligne, un suivi médical complet, et une interface graphique intuitive.

## ✅ Fonctionnalités principales

### 1. 🧑‍⚕️ Gestion des entités

- **Classe Patient**
  - Informations personnelles (nom, prénom, date de naissance, etc.)
  - Coordonnées de contact
  - Historique médical

- **Classe Médecin**
  - Informations professionnelles (nom, spécialité, disponibilités)
  - Liste des patients suivis

- **Classe Rendez-vous**
  - Date et heure
  - Médecin concerné
  - Patient concerné
  - Statut (planifié, annulé, terminé)

- **Classe Dossier Médical**
  - Historique des consultations
  - Traitements prescrits
  - Allergies, antécédents, etc.

- **Classe Prescription**
  - Médicaments prescrits
  - Posologie
  - Durée du traitement

---

### 2. 📅 Prise de rendez-vous en ligne

- Interface pour choisir un médecin, une date et une heure
- Affichage des créneaux disponibles
- Validation et enregistrement du rendez-vous

---

### 3. 🔔 Système de rappel automatique

- Rappel des rendez-vous par email ou SMS
- Notification des annulations ou modifications

---

### 4. 📂 Gestion des dossiers médicaux

- Visualisation et édition de l’historique médical
- Ajout de nouvelles consultations
- Archivage sécurisé

---

### 5. 💊 Gestion des prescriptions

- Création et édition des ordonnances
- Lien entre une consultation et une prescription
- Export en PDF possible

---

### 6. 🖥️ Interface graphique

- Application desktop intuitive
- Navigation fluide entre les différentes sections (patients, médecins, rendez-vous)
- Utilisation de composants modernes pour une meilleure expérience utilisateur

---

## 💡 Technologies utilisées

- **Langage :** Python 3.x  
- **Interface graphique :** Tkinter/CustomTkinter (à définir)  
- **Base de données :** fichier.Json 
- **Notifications :** 
  - Email via SMTP (`smtplib`)
  - SMS via API externe (par exemple Twilio)
- **Structure du projet :**
  - Programmation orientée objet (POO)
  - Architecture modulaire (séparation des classes, de l’interface, et de la logique métier)
