from datetime import date, time

class TimeSlot:
    def __init__(self, timeslot_id, doctor_id, date, start_time, end_time, is_reserved=False):
        self.timeslot_id = timeslot_id
        self.doctor_id = doctor_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.is_reserved = is_reserved

    def reserve(self):
        self.is_reserved = True

    def release(self):
        self.is_reserved = False

    def __str__(self):
        status = "Reserved" if self.is_reserved else "Available"
        return f"Time Slot {self.timeslot_id}: {self.date} from {self.start_time} to {self.end_time} ({status})" 