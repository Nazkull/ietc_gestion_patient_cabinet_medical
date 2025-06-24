import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
import json
import os
from typing import Optional

class EmailManager:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = None
        self.sender_password = None
        self.is_configured = False
        self.config_file = "data/email_config.json"
        self.load_configuration()
        
    def load_configuration(self):
        """Charge la configuration email depuis le fichier"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.sender_email = config.get('email')
                    self.sender_password = config.get('password')
                    self.is_configured = bool(self.sender_email and self.sender_password)
                    if self.is_configured:
                        logging.info(f"Configuration email chargée depuis {self.config_file}")
        except Exception as e:
            logging.error(f"Erreur lors du chargement de la configuration email: {e}")
        
    def save_configuration(self):
        """Sauvegarde la configuration email dans le fichier"""
        try:
            # Créer le dossier data s'il n'existe pas
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            config = {
                'email': self.sender_email,
                'password': self.sender_password
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
                
            logging.info(f"Configuration email sauvegardée dans {self.config_file}")
            
        except Exception as e:
            logging.error(f"Erreur lors de la sauvegarde de la configuration email: {e}")
        
    def configure(self, sender_email: str, sender_password: str):
        """Configure l'email manager pour l'envoi d'emails avec Gmail"""
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.is_configured = True
        self.save_configuration()  # Sauvegarder la configuration
        logging.info(f"Email manager configuré avec {sender_email}")
        
    def send_appointment_confirmation(self, to_email: str, appointment: dict, patient_name: str, doctor_name: str) -> bool:
        """Envoie un email de confirmation de rendez-vous"""
        # Formater la date et l'heure
        start_time = datetime.fromisoformat(appointment['start_time'])
        date_str = start_time.strftime('%d/%m/%Y')
        time_str = start_time.strftime('%H:%M')
        
        subject = "Confirmation de Rendez-vous"
        body = f"""
        <html>
        <body>
            <h2>Confirmation de Rendez-vous</h2>
            <p>Bonjour {patient_name},</p>
            
            <p>Votre rendez-vous a été confirmé avec succès :</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Date :</strong> {date_str}</p>
                <p><strong>Heure :</strong> {time_str}</p>
                <p><strong>Médecin :</strong> Dr. {doctor_name}</p>
                <p><strong>Raison :</strong> {appointment.get('reason', 'Consultation')}</p>
            </div>
            
            <p>Merci de vous présenter 10 minutes avant l'heure du rendez-vous.</p>
            
            <p>Cordialement,<br>
            <em>Équipe Médicale</em></p>
        </body>
        </html>
        """
        
        return self._send_email(to_email, subject, body)
        
    def send_appointment_cancellation(self, to_email: str, appointment: dict, patient_name: str, doctor_name: str) -> bool:
        """Envoie un email d'annulation de rendez-vous"""
        # Formater la date et l'heure
        start_time = datetime.fromisoformat(appointment['start_time'])
        date_str = start_time.strftime('%d/%m/%Y')
        time_str = start_time.strftime('%H:%M')
        
        subject = "Annulation de Rendez-vous"
        body = f"""
        <html>
        <body>
            <h2>Annulation de Rendez-vous</h2>
            <p>Bonjour {patient_name},</p>
            
            <p>Votre rendez-vous a été annulé :</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Date :</strong> {date_str}</p>
                <p><strong>Heure :</strong> {time_str}</p>
                <p><strong>Médecin :</strong> Dr. {doctor_name}</p>
                <p><strong>Raison :</strong> {appointment.get('reason', 'Consultation')}</p>
            </div>
            
            <p>Pour prendre un nouveau rendez-vous, veuillez contacter notre secrétariat.</p>
            
            <p>Cordialement,<br>
            <em>Équipe Médicale</em></p>
        </body>
        </html>
        """
        
        return self._send_email(to_email, subject, body)
        
    def send_reminder_email(self, to_email: str, appointment: dict, patient_name: str, doctor_name: str) -> bool:
        """Envoie un email de rappel de rendez-vous"""
        # Formater la date et l'heure
        start_time = datetime.fromisoformat(appointment['start_time'])
        date_str = start_time.strftime('%d/%m/%Y')
        time_str = start_time.strftime('%H:%M')
        
        subject = "Rappel de Rendez-vous - Demain"
        body = f"""
        <html>
        <body>
            <h2>Rappel de Rendez-vous</h2>
            <p>Bonjour {patient_name},</p>
            
            <p>Ceci est un rappel pour votre rendez-vous <strong>demain</strong> :</p>
            
            <div style="background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0;">
                <p><strong>Date :</strong> {date_str}</p>
                <p><strong>Heure :</strong> {time_str}</p>
                <p><strong>Médecin :</strong> Dr. {doctor_name}</p>
                <p><strong>Raison :</strong> {appointment.get('reason', 'Consultation')}</p>
            </div>
            
            <p>Merci de vous présenter 10 minutes avant l'heure du rendez-vous.</p>
            
            <p>Cordialement,<br>
            <em>Équipe Médicale</em></p>
        </body>
        </html>
        """
        
        return self._send_email(to_email, subject, body)
        
    def send_test_email(self, to_email: str) -> bool:
        """Envoie un email de test"""
        subject = "Test de Configuration - Système de Rendez-vous"
        body = f"""
        <html>
        <body>
            <h2>Test de Configuration Email</h2>
            <p>Cet email confirme que votre configuration email fonctionne correctement.</p>
            <p><strong>Date et heure :</strong> {datetime.now().strftime("%d/%m/%Y à %H:%M")}</p>
            <p>Si vous recevez cet email, votre configuration est opérationnelle !</p>
            <hr>
            <p><em>Système de Gestion de Rendez-vous Médicaux</em></p>
        </body>
        </html>
        """
        
        return self._send_email(to_email, subject, body)
        
    def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Envoie un email"""
        if not self.is_configured or not self.sender_email or not self.sender_password:
            logging.error("Email manager not properly configured")
            return False
            
        try:
            # Créer le message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Ajouter le corps du message
            msg.attach(MIMEText(body, 'html'))
            
            # Connexion au serveur SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            # Envoyer l'email
            text = msg.as_string()
            server.sendmail(self.sender_email, to_email, text)
            server.quit()
            
            logging.info(f"Email envoyé avec succès à {to_email}")
            return True
            
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'email: {e}")
            return False 