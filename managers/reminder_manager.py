import threading
import time
from datetime import datetime, timedelta
import logging
from typing import List, Dict, TYPE_CHECKING
from managers.email_manager import EmailManager
from managers.user_manager import UserManager

if TYPE_CHECKING:
    from managers.appointment_manager import AppointmentManager

class ReminderManager:
    def __init__(self, appointment_manager: 'AppointmentManager', user_manager: UserManager):
        self.appointment_manager = appointment_manager
        self.user_manager = user_manager
        self.email_manager = EmailManager()
        self.reminder_thread = None
        self.is_running = False
        self.sent_reminders = set()  # Pour éviter les doublons
        
    def start_reminder_service(self):
        """Démarre le service de rappels automatiques"""
        if self.is_running:
            logging.info("Service de rappels déjà en cours")
            return
            
        if not self.email_manager.is_configured:
            logging.error("Email manager non configuré")
            return
            
        self.is_running = True
        self.reminder_thread = threading.Thread(target=self._reminder_loop, daemon=True)
        self.reminder_thread.start()
        logging.info("Service de rappels démarré")
        
    def stop_reminder_service(self):
        """Arrête le service de rappels"""
        self.is_running = False
        if self.reminder_thread:
            self.reminder_thread.join(timeout=5)
        logging.info("Service de rappels arrêté")
        
    def _reminder_loop(self):
        """Boucle principale du service de rappels"""
        while self.is_running:
            try:
                self._check_and_send_reminders()
                # Attendre 1 heure avant la prochaine vérification
                time.sleep(3600)  # 3600 secondes = 1 heure
            except Exception as e:
                logging.error(f"Erreur dans la boucle de rappels: {e}")
                time.sleep(300)  # Attendre 5 minutes en cas d'erreur
                
    def _check_and_send_reminders(self):
        """Vérifie et envoie les rappels pour les rendez-vous de demain"""
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_date = tomorrow.date()
        
        # Obtenir tous les rendez-vous
        appointments = self.appointment_manager.get_all_appointments()
        
        for appointment in appointments:
            if appointment['status'] != 'planned':
                continue
                
            appointment_datetime = datetime.fromisoformat(appointment['start_time'])
            appointment_date = appointment_datetime.date()
            
            # Vérifier si c'est pour demain
            if appointment_date == tomorrow_date:
                self._send_reminder_for_appointment(appointment)
                
    def _send_reminder_for_appointment(self, appointment: Dict):
        """Envoie un rappel pour un rendez-vous spécifique"""
        appointment_id = appointment['appointment_id']
        patient_id = appointment['patient_id']
        reminder_key = f"{appointment_id}_{patient_id}"
        
        # Éviter les doublons
        if reminder_key in self.sent_reminders:
            return
            
        # Obtenir les informations du patient
        patient = self.user_manager.find_user_by_id(patient_id)
        if not patient or not patient.get('email'):
            logging.warning(f"Patient {patient_id} non trouvé ou sans email")
            return
            
        # Obtenir les informations du médecin
        doctor = self.user_manager.find_user_by_id(appointment['doctor_id'])
        if not doctor:
            logging.warning(f"Médecin {appointment['doctor_id']} non trouvé")
            return
            
        # Envoyer l'email de rappel
        patient_name = f"{patient.get('first_name', '')} {patient.get('last_name', '')}".strip()
        doctor_name = f"{doctor.get('first_name', '')} {doctor.get('last_name', '')}".strip()
        
        if self.email_manager.send_reminder_email(patient['email'], appointment, patient_name, doctor_name):
            self.sent_reminders.add(reminder_key)
            logging.info(f"Rappel envoyé pour le rendez-vous {appointment_id} à {patient['email']}")
            
    def send_manual_reminders_for_tomorrow(self) -> Dict:
        """Envoie manuellement les rappels pour les rendez-vous de demain"""
        try:
            if not self.email_manager.is_configured:
                return {
                    "success": False,
                    "message": "Email manager non configuré",
                    "count": 0
                }
                
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow_date = tomorrow.date()
            
            # Obtenir tous les rendez-vous
            appointments = self.appointment_manager.get_all_appointments()
            reminders_sent = 0
            
            for appointment in appointments:
                if appointment['status'] != 'planned':
                    continue
                    
                appointment_datetime = datetime.fromisoformat(appointment['start_time'])
                appointment_date = appointment_datetime.date()
                
                # Vérifier si c'est pour demain
                if appointment_date == tomorrow_date:
                    if self._send_manual_reminder(appointment):
                        reminders_sent += 1
                        
            if reminders_sent > 0:
                return {
                    "success": True,
                    "message": f"Rappels envoyés pour {reminders_sent} rendez-vous de demain",
                    "count": reminders_sent
                }
            else:
                return {
                    "success": True,
                    "message": "Aucun rendez-vous confirmé pour demain",
                    "count": 0
                }
                
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi manuel des rappels: {e}")
            return {
                "success": False,
                "message": f"Erreur: {str(e)}",
                "count": 0
            }
            
    def _send_manual_reminder(self, appointment: Dict) -> bool:
        """Envoie un rappel manuel pour un rendez-vous"""
        try:
            patient_id = appointment['patient_id']
            
            # Obtenir les informations du patient
            patient = self.user_manager.find_user_by_id(patient_id)
            if not patient or not patient.get('email'):
                logging.warning(f"Patient {patient_id} non trouvé ou sans email")
                return False
                
            # Obtenir les informations du médecin
            doctor = self.user_manager.find_user_by_id(appointment['doctor_id'])
            if not doctor:
                logging.warning(f"Médecin {appointment['doctor_id']} non trouvé")
                return False
                
            # Envoyer l'email de rappel
            patient_name = f"{patient.get('first_name', '')} {patient.get('last_name', '')}".strip()
            doctor_name = f"{doctor.get('first_name', '')} {doctor.get('last_name', '')}".strip()
            
            return self.email_manager.send_reminder_email(patient['email'], appointment, patient_name, doctor_name)
            
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi du rappel manuel: {e}")
            return False
        
    def send_confirmation_email(self, appointment: Dict):
        """Envoie un email de confirmation de rendez-vous"""
        try:
            patient_id = appointment['patient_id']
            
            # Obtenir les informations du patient
            patient = self.user_manager.find_user_by_id(patient_id)
            if not patient or not patient.get('email'):
                logging.warning(f"Patient {patient_id} non trouvé ou sans email")
                return False
                
            # Obtenir les informations du médecin
            doctor = self.user_manager.find_user_by_id(appointment['doctor_id'])
            if not doctor:
                logging.warning(f"Médecin {appointment['doctor_id']} non trouvé")
                return False
                
            # Envoyer l'email de confirmation
            patient_name = f"{patient.get('first_name', '')} {patient.get('last_name', '')}".strip()
            doctor_name = f"{doctor.get('first_name', '')} {doctor.get('last_name', '')}".strip()
            
            return self.email_manager.send_appointment_confirmation(patient['email'], appointment, patient_name, doctor_name)
            
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'email de confirmation: {e}")
            return False
            
    def send_cancellation_email(self, appointment: Dict):
        """Envoie un email d'annulation de rendez-vous"""
        try:
            patient_id = appointment['patient_id']
            
            # Obtenir les informations du patient
            patient = self.user_manager.find_user_by_id(patient_id)
            if not patient or not patient.get('email'):
                logging.warning(f"Patient {patient_id} non trouvé ou sans email")
                return False
                
            # Obtenir les informations du médecin
            doctor = self.user_manager.find_user_by_id(appointment['doctor_id'])
            if not doctor:
                logging.warning(f"Médecin {appointment['doctor_id']} non trouvé")
                return False
                
            # Envoyer l'email d'annulation
            patient_name = f"{patient.get('first_name', '')} {patient.get('last_name', '')}".strip()
            doctor_name = f"{doctor.get('first_name', '')} {doctor.get('last_name', '')}".strip()
            
            return self.email_manager.send_appointment_cancellation(patient['email'], appointment, patient_name, doctor_name)
            
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'email d'annulation: {e}")
            return False 