from datetime import datetime
from typing import Optional, Union

class Notification:
    def __init__(self, notification_id: str, user_id: str, title: str, message: str, 
                 notification_type: str, status: str = "unread", created_at: Optional[Union[datetime, str]] = None):
        self.notification_id = notification_id
        self.user_id = user_id
        self.title = title
        self.message = message
        self.notification_type = notification_type  # "appointment_confirmation", "reminder", "status_change", "system"
        self.status = status  # "unread", "read", "sent"
        
        if isinstance(created_at, str):
            self.created_at = datetime.fromisoformat(created_at)
        elif created_at is None:
            self.created_at = datetime.now()
        else:
            self.created_at = created_at
    
    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "user_id": self.user_id,
            "title": self.title,
            "message": self.message,
            "notification_type": self.notification_type,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            notification_id=data["notification_id"],
            user_id=data["user_id"],
            title=data["title"],
            message=data["message"],
            notification_type=data["notification_type"],
            status=data.get("status", "unread"),
            created_at=data.get("created_at")
        )
    
    def mark_as_read(self):
        self.status = "read"
    
    def mark_as_sent(self):
        self.status = "sent"

    def send(self):
        self.sent_date = datetime.now()
        # Logic to send the notification
        print(f"Sending {self.notification_type} to {self.user_id}: {self.message}")

    def __str__(self):
        return f"Notification for {self.user_id}: {self.message}" 