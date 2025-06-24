from managers.storage_manager import StorageManager
from datetime import datetime

class ScheduleManager:
    def __init__(self, storage):
        self.storage = storage
        self.timeslots_file = 'timeslots.json'
        self.timeslots = self._load()

    def _load(self):
        """charge les créneaux depuis le fichier"""
        return self.storage.load_data(self.timeslots_file)

    def _save(self):
        """sauvegarde les créneaux"""
        self.storage.save_data(self.timeslots_file, self.timeslots)

    def add_availability(self, doctor_id, start_time, end_time):
        """ajoute un créneau disponible pour un docteur"""
        timeslot_id = len(self.timeslots) + 1
        new_slot = {
            "timeslot_id": timeslot_id,
            "doctor_id": doctor_id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "is_reserved": False
        }
        self.timeslots.append(new_slot)
        self._save()
        print(f"Disponibilité ajoutée pour Dr {doctor_id} de {start_time} à {end_time}.")
        return new_slot

    def get_doctor_availability(self, doctor_id):
        """récupère les créneaux libres d'un docteur"""
        return [ts for ts in self.timeslots if ts['doctor_id'] == doctor_id and not ts['is_reserved']]

    def get_doctor_schedule(self, doctor_id):
        """récupère tous les créneaux d'un docteur"""
        return [ts for ts in self.timeslots if ts['doctor_id'] == doctor_id]

    def reserve_timeslot(self, doctor_id, start_time):
        """réserve un créneau"""
        for slot in self.timeslots:
            if slot['doctor_id'] == doctor_id and slot['start_time'] == start_time.isoformat():
                if not slot['is_reserved']:
                    slot['is_reserved'] = True
                    self._save()
                    return True
                else:
                    return False
        return False

    def unreserve_timeslot(self, doctor_id, start_time_iso):
        """libère un créneau"""
        for slot in self.timeslots:
            if slot['doctor_id'] == doctor_id and slot['start_time'] == start_time_iso:
                if slot['is_reserved']:
                    slot['is_reserved'] = False
                    self._save()
                    return True
                else:
                    return False
        return False

    def block_timeslot(self, doctor_id, start_time, end_time):
        """bloque un créneau"""
        for slot in self.timeslots:
            if slot['doctor_id'] == doctor_id and slot['start_time'] == start_time.isoformat():
                if not slot['is_reserved']:
                    slot['is_reserved'] = True
                    self._save()
                    return True
                else:
                    return False
        return False

    def unblock_timeslot(self, doctor_id, start_time_iso):
        """débloque un créneau"""
        for slot in self.timeslots:
            if slot['doctor_id'] == doctor_id and slot['start_time'] == start_time_iso:
                if slot['is_reserved']:
                    slot['is_reserved'] = False
                    self._save()
                    return True
                else:
                    return False
        return False 