from managers.storage_manager import StorageManager
from managers.schedule_manager import ScheduleManager
from managers.notification_manager import NotificationManager
from managers.user_manager import UserManager
from managers.reminder_manager import ReminderManager
from models.appointment import Appointment
from datetime import datetime, timedelta
import logging
from typing import List, Dict

class AppointmentManager:
    def __init__(self, storage_manager):
        self.storage_manager = storage_manager
        self.schedule_manager = ScheduleManager(storage_manager)
        self.notification_manager = NotificationManager(storage_manager)
        self.user_manager = UserManager(storage_manager)
        self.reminder_manager = ReminderManager(self, self.user_manager)
        self.appointments_file = 'appointments.json'
        self.appointments = self._load_appointments()

    def _load_appointments(self):
        """Loads appointments from the JSON file."""
        return self.storage_manager.load_data(self.appointments_file)

    def _save_appointments(self):
        """Saves the current list of appointments to the JSON file."""
        self.storage_manager.save_data(self.appointments_file, self.appointments)

    def reload_appointments(self):
        """Reloads appointments from the JSON file."""
        self.appointments = self._load_appointments()

    def _check_time(self, start_time, end_time):
        """vérifie les contraintes de temps"""
        now = datetime.now()
        
        # vérifier que c'est dans le futur
        if start_time <= now:
            return False, "Le rdv doit être dans le futur"
        
        # vérifier que c'est pas trop loin (1 an max)
        if start_time > now + timedelta(days=365):
            return False, "Le rdv ne peut pas être à plus d'1 an"
        
        # vérifier que la fin est après le début
        if end_time <= start_time:
            return False, "L'heure de fin doit être après le début"
        
        return True, "OK"

    def _check_conflicts(self, doctor_id, start_time, end_time, exclude_id=None):
        """vérifie les conflits de planning"""
        for appt in self.appointments:
            if exclude_id and appt['appointment_id'] == exclude_id:
                continue
                
            if appt['doctor_id'] == doctor_id and appt['status'] in ['pending', 'planned']:
                existing_start = datetime.fromisoformat(appt['start_time'])
                existing_end = datetime.fromisoformat(appt['end_time'])
                
                if (start_time < existing_end and end_time > existing_start):
                    return True, f"Conflit avec rdv {appt['appointment_id']}"
        
        return False, "Pas de conflit"

    def _get_next_id(self):
        """génère un nouvel id de rdv"""
        if not self.appointments:
            return "APT-1"
        
        max_id = 0
        for app in self.appointments:
            try:
                app_id_str = str(app.get('appointment_id', 0))
                if app_id_str.startswith('APT-'):
                    app_id_num = int(app_id_str.split('-')[-1])
                else:
                    app_id_num = int(app_id_str)
                
                if app_id_num > max_id:
                    max_id = app_id_num
            except:
                continue
        
        return f"APT-{max_id + 1}"

    def book_appointment(self, patient_id, doctor_id, start_time, end_time, reason, auto_confirm=False):
        """prend un nouveau rdv"""
        try:
            # validations
            if not all([patient_id, doctor_id, start_time, end_time, reason]):
                return False, "Tous les champs sont requis"
            
            # vérifier le temps
            is_valid, msg = self._check_time(start_time, end_time)
            if not is_valid:
                return False, msg
            
            # vérifier les conflits
            has_conflict, conflict_msg = self._check_conflicts(doctor_id, start_time, end_time)
            if has_conflict:
                return False, conflict_msg
            
            # créer le rdv
            appointment_id = self._get_next_id()
            status = 'planned' if auto_confirm else 'pending'
            
            appointment = {
                'appointment_id': appointment_id,
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'start_time': start_time.isoformat(),
                'end_time': end_time.isoformat(),
                'reason': reason,
                'status': status,
                'created_at': datetime.now().isoformat(),
                'booked_by_patient': auto_confirm
            }
            
            if auto_confirm:
                appointment['confirmed_at'] = datetime.now().isoformat()
            
            self.appointments.append(appointment)
            self._save_appointments()
            
            # créer les notifs
            self._create_notifs(appointment)
            
            # envoyer email si confirmé
            if auto_confirm:
                self.reminder_manager.send_confirmation_email(appointment)
            
            print(f"Rdv {appointment_id} pris avec succès")
            return True, f"Rendez-vous {appointment_id} pris avec succès"
            
        except Exception as e:
            print(f"Erreur prise rdv: {str(e)}")
            return False, f"Erreur lors de la prise de rendez-vous: {str(e)}"

    def _create_notifs(self, appointment):
        """crée les notifications pour un nouveau rdv"""
        try:
            # récupérer les infos users
            patient = self.user_manager.get_user(appointment['patient_id'])
            doctor = self.user_manager.get_user(appointment['doctor_id'])
            
            date_str = datetime.fromisoformat(appointment['start_time']).strftime('%d/%m/%Y')
            time_str = datetime.fromisoformat(appointment['start_time']).strftime('%H:%M')
            
            # nom du médecin
            doctor_name = f"{doctor.get('first_name', 'Dr.')} {doctor.get('last_name', '')}" if doctor else "le médecin"
            
            if appointment['status'] == 'planned':
                # rdv confirmé
                self.notification_manager.create_appointment_confirmation(
                    appointment['patient_id'],
                    appointment['appointment_id'],
                    doctor_name,
                    date_str,
                    time_str
                )
            else:
                # rdv en attente
                self.notification_manager.create_notification(
                    appointment['patient_id'],
                    "Rendez-vous en Attente",
                    f"Votre rdv avec {doctor_name} du {date_str} à {time_str} est en attente de confirmation.",
                    "appointment_pending"
                )
            
            # notif pour le médecin
            patient_name = f"{patient.get('first_name', '')} {patient.get('last_name', '')}" if patient else "le patient"
            self.notification_manager.create_notification(
                appointment['doctor_id'],
                "Nouveau Rendez-vous",
                f"Un nouveau rdv a été pris par {patient_name} pour le {date_str} à {time_str}. Raison: {appointment['reason']}",
                "new_appointment"
            )
            
        except Exception as e:
            print(f"Erreur création notifs: {e}")

    def cancel_appointment(self, appointment_id):
        """annule un rdv"""
        try:
            appointment = self._find(appointment_id)
            if not appointment:
                return False, "Rdv non trouvé"
            
            old_status = appointment['status']
            appointment['status'] = 'cancelled'
            appointment['cancelled_at'] = datetime.now().isoformat()
            self._save_appointments()
            
            # créer notifs d'annulation
            self._create_cancel_notifs(appointment)
            
            print(f"Rdv {appointment_id} annulé")
            return True, f"Rendez-vous {appointment_id} annulé"
            
        except Exception as e:
            print(f"Erreur annulation: {e}")
            return False, f"Erreur lors de l'annulation: {str(e)}"

    def _create_cancel_notifs(self, appointment):
        """crée les notifs d'annulation"""
        try:
            patient = self.user_manager.get_user(appointment['patient_id'])
            doctor = self.user_manager.get_user(appointment['doctor_id'])
            
            date_str = datetime.fromisoformat(appointment['start_time']).strftime('%d/%m/%Y')
            time_str = datetime.fromisoformat(appointment['start_time']).strftime('%H:%M')
            
            # notif patient
            doctor_name = f"{doctor.get('first_name', 'Dr.')} {doctor.get('last_name', '')}" if doctor else "le médecin"
            self.notification_manager.create_notification(
                appointment['patient_id'],
                "Rendez-vous Annulé",
                f"Votre rdv avec {doctor_name} du {date_str} à {time_str} a été annulé.",
                "appointment_cancelled"
            )
            
            # notif médecin
            patient_name = f"{patient.get('first_name', '')} {patient.get('last_name', '')}" if patient else "le patient"
            self.notification_manager.create_notification(
                appointment['doctor_id'],
                "Rendez-vous Annulé",
                f"Le rdv avec {patient_name} du {date_str} à {time_str} a été annulé.",
                "appointment_cancelled"
            )
            
        except Exception as e:
            print(f"Erreur notifs annulation: {e}")

    def delete_appointment(self, appointment_id):
        """supprime un rdv"""
        try:
            appointment = self._find(appointment_id)
            if not appointment:
                return False, "Rdv non trouvé"
            
            # créer notifs de suppression
            self._create_delete_notifs(appointment)
            
            # supprimer du fichier
            self.appointments = [app for app in self.appointments if app['appointment_id'] != appointment_id]
            self._save_appointments()
            
            print(f"Rdv {appointment_id} supprimé")
            return True, f"Rendez-vous {appointment_id} supprimé"
            
        except Exception as e:
            print(f"Erreur suppression: {e}")
            return False, f"Erreur lors de la suppression: {str(e)}"

    def _create_delete_notifs(self, appointment):
        """crée les notifs de suppression"""
        try:
            patient = self.user_manager.get_user(appointment['patient_id'])
            doctor = self.user_manager.get_user(appointment['doctor_id'])
            
            date_str = datetime.fromisoformat(appointment['start_time']).strftime('%d/%m/%Y')
            time_str = datetime.fromisoformat(appointment['start_time']).strftime('%H:%M')
            
            # notif patient
            doctor_name = f"{doctor.get('first_name', 'Dr.')} {doctor.get('last_name', '')}" if doctor else "le médecin"
            self.notification_manager.create_notification(
                appointment['patient_id'],
                "Rendez-vous Supprimé",
                f"Votre rdv avec {doctor_name} du {date_str} à {time_str} a été supprimé.",
                "appointment_deleted"
            )
            
            # notif médecin
            patient_name = f"{patient.get('first_name', '')} {patient.get('last_name', '')}" if patient else "le patient"
            self.notification_manager.create_notification(
                appointment['doctor_id'],
                "Rendez-vous Supprimé",
                f"Le rdv avec {patient_name} du {date_str} à {time_str} a été supprimé.",
                "appointment_deleted"
            )
            
        except Exception as e:
            print(f"Erreur notifs suppression: {e}")

    def validate_appointment(self, appointment_id):
        """valide un rdv"""
        try:
            appointment = self._find(appointment_id)
            if not appointment:
                return False, "Rdv non trouvé"
            
            if appointment['status'] != 'pending':
                return False, "Le rdv n'est pas en attente"
            
            appointment['status'] = 'planned'
            appointment['confirmed_at'] = datetime.now().isoformat()
            self._save_appointments()
            
            # créer notifs de validation
            self._create_validation_notifs(appointment)
            
            # envoyer email de confirmation
            self.reminder_manager.send_confirmation_email(appointment)
            
            print(f"Rdv {appointment_id} validé")
            return True, f"Rendez-vous {appointment_id} validé"
            
        except Exception as e:
            print(f"Erreur validation: {e}")
            return False, f"Erreur lors de la validation: {str(e)}"

    def _create_validation_notifs(self, appointment):
        """crée les notifs de validation"""
        try:
            patient = self.user_manager.get_user(appointment['patient_id'])
            doctor = self.user_manager.get_user(appointment['doctor_id'])
            
            date_str = datetime.fromisoformat(appointment['start_time']).strftime('%d/%m/%Y')
            time_str = datetime.fromisoformat(appointment['start_time']).strftime('%H:%M')
            
            # notif patient
            doctor_name = f"{doctor.get('first_name', 'Dr.')} {doctor.get('last_name', '')}" if doctor else "le médecin"
            self.notification_manager.create_appointment_confirmation(
                appointment['patient_id'],
                appointment['appointment_id'],
                doctor_name,
                date_str,
                time_str
            )
            
            # notif médecin
            patient_name = f"{patient.get('first_name', '')} {patient.get('last_name', '')}" if patient else "le patient"
            self.notification_manager.create_notification(
                appointment['doctor_id'],
                "Rendez-vous Confirmé",
                f"Le rdv avec {patient_name} du {date_str} à {time_str} a été confirmé.",
                "appointment_confirmed"
            )
            
        except Exception as e:
            print(f"Erreur notifs validation: {e}")

    def get_appointments_for_patient(self, patient_id):
        """récupère les rdv d'un patient"""
        return [app for app in self.appointments if app['patient_id'] == patient_id]

    def get_appointments_for_doctor(self, doctor_id):
        """récupère les rdv d'un docteur"""
        return [app for app in self.appointments if app['doctor_id'] == doctor_id]

    def get_all_appointments(self):
        """récupère tous les rdv"""
        return self.appointments

    def _find(self, appointment_id):
        """trouve un rdv par id"""
        for app in self.appointments:
            if app['appointment_id'] == appointment_id:
                return app
        return None

    def get_appointments_by_status(self, status):
        """récupère les rdv par statut"""
        return [app for app in self.appointments if app['status'] == status] 