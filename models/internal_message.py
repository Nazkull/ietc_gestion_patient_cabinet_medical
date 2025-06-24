from datetime import datetime

class InternalMessage:
    def __init__(self, message_id, sender_id, recipient_id, subject, body, sent_date=None, is_read=False):
        self.message_id = message_id
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.subject = subject
        self.body = body
        self.sent_date = sent_date
        self.is_read = is_read

    def send(self):
        self.sent_date = datetime.now()
        # Logic to send the message
        print(f"Message from {self.sender_id} to {self.recipient_id} sent.")

    def mark_as_read(self):
        self.is_read = True

    def __str__(self):
        return f"Message from {self.sender_id} to {self.recipient_id}: {self.subject}" 