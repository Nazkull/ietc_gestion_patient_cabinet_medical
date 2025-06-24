class ConsultationRoom:
    def __init__(self, room_id, room_number, equipment=""):
        self.room_id = room_id
        self.room_number = room_number
        self.equipment = equipment
        self.occupied = False

    def occupy(self):
        self.occupied = True

    def release(self):
        self.occupied = False

    def __str__(self):
        status = "Occupée" if self.occupied else "Libre"
        return f"Salle {self.room_number} ({status})" 