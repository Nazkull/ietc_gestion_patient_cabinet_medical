# Centre Médical Coruscant - Système de Gestion de Rendez-vous

## 📋 Description

Application de gestion de rendez-vous médicaux développée en Python avec interface graphique Tkinter. Le système permet aux patients, médecins et secrétaires de gérer les rendez-vous médicaux de manière efficace.

## 🚀 Fonctionnalités

### 👥 Gestion des Utilisateurs
- **Inscription** : Patients, médecins et secrétaires
- **Connexion sécurisée** avec hashage des mots de passe
- **Validation des données** (email, téléphone, sécurité sociale)
- **Profils personnalisés** selon le rôle

### 📅 Gestion des Rendez-vous
- **Réservation** de rendez-vous avec validation des conflits
- **Annulation** de rendez-vous
- **Confirmation** par les secrétaires
- **Consultation** des plannings

### 🎨 Interface Utilisateur
- **Design moderne** avec thème Star Wars
- **Navigation intuitive** entre les écrans
- **Validation en temps réel** des formulaires
- **Messages d'erreur** informatifs

## 🏗️ Architecture du Projet

```
projet Python/
├── assets/                 # Images et ressources
├── data/                   # Fichiers de données JSON
├── gui/                    # Interface graphique
│   ├── main_app.py        # Application principale
│   ├── login_frame.py     # Écran de connexion
│   ├── register_frame.py  # Écran d'inscription
│   ├── dashboard_frames.py # Tableaux de bord
│   └── sidebar_frame.py   # Barre latérale
├── managers/              # Gestionnaires métier
│   ├── user_manager.py    # Gestion des utilisateurs
│   ├── appointment_manager.py # Gestion des rendez-vous
│   ├── schedule_manager.py # Gestion des plannings
│   └── storage_manager.py # Gestion du stockage
├── models/                # Modèles de données
├── config.py             # Configuration centralisée
├── main.py               # Version CLI
├── run_gui.py            # Lancement GUI
└── README.md             # Documentation
```

## 🛠️ Technologies Utilisées

- **Python 3.x** : Langage principal
- **Tkinter** : Interface graphique
- **JSON** : Stockage des données
- **PIL/Pillow** : Gestion des images
- **Hashlib** : Sécurisation des mots de passe
- **Logging** : Journalisation des événements

## 📦 Installation

1. **Cloner le projet** :
```bash
git clone <repository-url>
cd "projet Python"
```

2. **Installer les dépendances** :
```bash
pip install pillow
```

3. **Lancer l'application** :
```bash
# Version graphique
python run_gui.py

# Version ligne de commande
python main.py
```

## 👤 Utilisation

### 🔐 Connexion
1. Lancez l'application
2. Cliquez sur "S'inscrire" pour créer un compte
3. Remplissez le formulaire avec vos informations
4. Connectez-vous avec votre email et mot de passe

### 📅 Prendre un Rendez-vous (Patients)
1. Connectez-vous en tant que patient
2. Cliquez sur "Appointments" dans le menu
3. Sélectionnez un médecin et une date
4. Confirmez votre rendez-vous

### 👨‍⚕️ Gérer les Rendez-vous (Médecins)
1. Connectez-vous en tant que médecin
2. Consultez votre planning
3. Ajoutez vos disponibilités
4. Gérez vos rendez-vous

### 📋 Administration (Secrétaires)
1. Connectez-vous en tant que secrétaire
2. Consultez tous les rendez-vous
3. Validez ou annulez les rendez-vous
4. Gérez les plannings

## 🔒 Sécurité

- **Mots de passe hashés** avec SHA-256
- **Validation des données** côté client et serveur
- **Gestion des erreurs** robuste
- **Journalisation** des actions importantes

## 🎯 Fonctionnalités Avancées

### ✅ Implémentées
- [x] Interface graphique moderne
- [x] Gestion des utilisateurs
- [x] Système de rendez-vous
- [x] Validation des données
- [x] Sécurisation des mots de passe
- [x] Gestion des erreurs
- [x] Journalisation
- [x] Configuration centralisée

### 🔄 En Développement
- [ ] Notifications par email
- [ ] Export des données
- [ ] Statistiques avancées
- [ ] Interface mobile
- [ ] Base de données SQL

## 🐛 Dépannage

### Problèmes Courants

1. **Erreur de module** :
```bash
pip install pillow
```

2. **Fichier de données corrompu** :
- Supprimez le fichier `data/users.json`
- Recréez votre compte

3. **Interface graphique ne se lance pas** :
- Vérifiez que Tkinter est installé
- Redémarrez l'application

## 📝 Journal des Modifications

### Version 1.0.0
- ✅ Interface graphique complète
- ✅ Gestion des utilisateurs
- ✅ Système de rendez-vous
- ✅ Validation des données
- ✅ Sécurisation

## 👨‍💻 Développement

### Structure du Code
- **Modèles** : Classes de données
- **Gestionnaires** : Logique métier
- **Interface** : Composants GUI
- **Configuration** : Paramètres centralisés

### Bonnes Pratiques
- Code modulaire et réutilisable
- Gestion d'erreurs robuste
- Documentation complète
- Tests unitaires (à implémenter)

## 📞 Support

Pour toute question ou problème :
1. Consultez la documentation
2. Vérifiez les logs dans `app.log`
3. Contactez l'équipe de développement

---

**Développé avec ❤️ pour la gestion médicale moderne** 