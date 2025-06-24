from datetime import datetime

class AppointmentHistory:
    def __init__(self, history_id, appointment_id, action_type, action_by_user_id, details, action_date=None):
        self.history_id = history_id
        self.appointment_id = appointment_id
        self.action_type = action_type  # e.g., 'Creation', 'Modification', 'Cancellation'
        self.action_by_user_id = action_by_user_id
        self.details = details
        self.action_date = action_date if action_date else datetime.now()

    def record_action(self):
        # This method could be used to save the history record to a file
        print(f"Action '{self.action_type}' recorded for appointment {self.appointment_id} by user {self.action_by_user_id}.")

    def __str__(self):
        return f"History: {self.action_date.strftime('%Y-%m-%d %H:%M')} - Appointment {self.appointment_id} - {self.action_type} by {self.action_by_user_id}" 