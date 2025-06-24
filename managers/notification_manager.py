import json
from datetime import datetime, timedelta
from models.notification import Notification
from managers.storage_manager import StorageManager

class NotificationManager:
    def __init__(self, storage):
        self.storage = storage
        self.notifications_file = "notifications.json"
        self.notifications = []
        self.load_notifications()
    
    def load_notifications(self):
        """charge les notifs depuis le fichier"""
        try:
            data = self.storage.load_data(self.notifications_file)
            self.notifications = [Notification.from_dict(notif) for notif in data]
        except:
            self.notifications = []
    
    def save_notifications(self):
        """sauvegarde les notifs"""
        notifications_data = [notif.to_dict() for notif in self.notifications]
        self.storage.save_data(self.notifications_file, notifications_data)
    
    def create_notification(self, user_id, title, message, notification_type="system"):
        """crée une nouvelle notif"""
        notification_id = f"NOTIF-{len(self.notifications) + 1}"
        notification = Notification(
            notification_id=notification_id,
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type
        )
        self.notifications.append(notification)
        self.save_notifications()
        return notification
    
    def get_notifications_for_user(self, user_id, status=None):
        """récupère les notifs d'un user"""
        notifications = []
        for notif in self.notifications:
            if notif.user_id == user_id:
                if status is None or notif.status == status:
                    notifications.append(notif)
        
        return sorted(notifications, key=lambda x: x.created_at, reverse=True)
    
    def mark_notification_as_read(self, notification_id):
        """marque une notif comme lue"""
        for notif in self.notifications:
            if notif.notification_id == notification_id:
                notif.mark_as_read()
                self.save_notifications()
                return True
        return False
    
    def mark_notification_as_sent(self, notification_id):
        """marque une notif comme envoyée"""
        for notif in self.notifications:
            if notif.notification_id == notification_id:
                notif.mark_as_sent()
                self.save_notifications()
                return True
        return False
    
    def delete_notification(self, notification_id):
        """supprime une notif"""
        for i, notif in enumerate(self.notifications):
            if notif.notification_id == notification_id:
                del self.notifications[i]
                self.save_notifications()
                return True
        return False
    
    def get_unread_count(self, user_id):
        """compte les notifs non lues d'un user"""
        return len(self.get_notifications_for_user(user_id, status="unread"))
    
    # méthodes spécialisées
    def create_appointment_confirmation(self, user_id, appointment_id, doctor_name, date, time):
        """crée une notif de confirmation de rdv"""
        title = "Confirmation de Rendez-vous"
        message = f"Votre rdv avec {doctor_name} le {date} à {time} a été confirmé. ID: {appointment_id}"
        return self.create_notification(user_id, title, message, "appointment_confirmation")
    
    def create_appointment_reminder(self, user_id, doctor_name, date, time):
        """crée une notif de rappel de rdv"""
        title = "Rappel de Rendez-vous"
        message = f"Rappel : Vous avez un rdv avec {doctor_name} le {date} à {time}"
        return self.create_notification(user_id, title, message, "reminder")
    
    def create_status_change_notification(self, user_id, appointment_id, old_status, new_status):
        """crée une notif de changement de statut"""
        title = "Changement de Statut"
        message = f"Le statut de votre rdv {appointment_id} a changé de '{old_status}' à '{new_status}'"
        return self.create_notification(user_id, title, message, "status_change")
    
    def create_system_notification(self, user_id, title, message):
        """crée une notif système"""
        return self.create_notification(user_id, title, message, "system")
    
    def send_appointment_reminders(self, appointment_manager, user_manager):
        """envoie des rappels pour les rdv du lendemain"""
        tomorrow = datetime.now() + timedelta(days=1)
        appointments = appointment_manager.get_appointments_by_date(tomorrow.date())
        
        for appointment in appointments:
            patient_id = appointment.get('patient_id')
            doctor_id = appointment.get('doctor_id')
            
            if patient_id and doctor_id:
                patient = user_manager.get_user(patient_id)
                doctor = user_manager.get_user(doctor_id)
                
                if patient and doctor:
                    start_time = datetime.fromisoformat(appointment['start_time'])
                    date_str = start_time.strftime('%d/%m/%Y')
                    time_str = start_time.strftime('%H:%M')
                    
                    self.create_appointment_reminder(
                        patient_id, 
                        f"{doctor['first_name']} {doctor['last_name']}", 
                        date_str, 
                        time_str
                    ) 