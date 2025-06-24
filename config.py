"""
Configuration pour le système de gestion de rdv médicaux
"""

import os
from datetime import timedelta

# Infos de l'app
APP_NAME = "Centre Médical Coruscant"
APP_VERSION = "1.0.0"
APP_DESC = "Services de Santé de la République"

# Chemins des fichiers
DATA_DIR = "data"
ASSETS_DIR = "assets"
LOG_FILE = "app.log"

# Fichiers de données
USERS_FILE = "users.json"
APPOINTMENTS_FILE = "appointments.json"
TIMESLOTS_FILE = "timeslots.json"

# Paramètres GUI
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768
WINDOW_TITLE = f"{APP_NAME} - {APP_DESC}"

# Couleurs (thème Star Wars)
COLORS = {
    'primary': '#ffd700',      # Or
    'secondary': '#1a1a2e',    # Bleu foncé
    'background': '#0a0a0a',   # Fond sombre
    'text': '#ffffff',         # Blanc
    'error': '#ff4444',        # Rouge
    'success': '#44ff44',      # Vert
    'warning': '#ffaa00'       # Orange
}

# Paramètres de validation
VALIDATION = {
    'min_password_length': 6,
    'min_phone_length': 10,
    'min_ssn_length': 10,
    'max_appointment_advance_days': 365,
    'appointment_duration_hours': 1
}

# Heures de travail
WORKING_HOURS = {
    'start': 8,    # 8h
    'end': 18      # 18h
}

# Configuration logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file_handler': True,
    'console_handler': True
}

# Paramètres sécurité
SECURITY = {
    'password_hash_algorithm': 'sha256',
    'session_timeout_minutes': 30
}

# Statuts des rdv
APPOINTMENT_STATUS = {
    'PENDING': 'pending',
    'CONFIRMED': 'confirmed',
    'CANCELLED': 'cancelled',
    'COMPLETED': 'completed'
}

# Rôles utilisateurs
USER_ROLES = {
    'PATIENT': 'Patient',
    'DOCTOR': 'Doctor',
    'SECRETARY': 'Secretary'
}

# Messages d'erreur
ERROR_MESSAGES = {
    'invalid_email': 'Format d\'email invalide.',
    'invalid_phone': 'Format de téléphone invalide.',
    'invalid_ssn': 'Format de numéro de sécu invalide.',
    'invalid_date': 'Format de date invalide (YYYY-MM-DD).',
    'weak_password': f'Le mot de passe doit contenir au moins {VALIDATION["min_password_length"]} caractères.',
    'missing_fields': 'Veuillez remplir tous les champs obligatoires.',
    'email_exists': 'Un utilisateur avec cet email existe déjà.',
    'login_failed': 'Email ou mot de passe incorrect.',
    'appointment_conflict': 'Conflit de rdv détecté.',
    'past_appointment': 'Impossible de prendre rdv dans le passé.',
    'too_far_future': f'Impossible de prendre rdv plus de {VALIDATION["max_appointment_advance_days"]} jours à l\'avance.'
}

# Messages de succès
SUCCESS_MESSAGES = {
    'registration': 'Compte créé avec succès!',
    'login': 'Connexion réussie!',
    'appointment_booked': 'Rdv réservé avec succès!',
    'appointment_cancelled': 'Rdv annulé avec succès.',
    'appointment_confirmed': 'Rdv confirmé avec succès.'
}

def get_data_file_path(filename):
    """retourne le chemin complet vers un fichier de données"""
    return os.path.join(DATA_DIR, filename)

def get_asset_file_path(filename):
    """retourne le chemin complet vers un fichier asset"""
    return os.path.join(ASSETS_DIR, filename)

def ensure_directories():
    """s'assure que les dossiers requis existent"""
    directories = [DATA_DIR, ASSETS_DIR]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory) 