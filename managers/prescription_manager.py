import json
import logging
from datetime import datetime
from models.prescription import Prescription

class PrescriptionManager:
    def __init__(self, storage_manager):
        self.storage_manager = storage_manager
        self.prescriptions = self._load_prescriptions()
    
    def _load_prescriptions(self):
        """Charge les ordonnances depuis le fichier JSON."""
        try:
            data = self.storage_manager.load_data('prescriptions.json')
            prescriptions = []
            for prescription_data in data:
                prescription = Prescription.from_dict(prescription_data)
                prescriptions.append(prescription)
            logging.info("Successfully loaded prescriptions.json")
            return prescriptions
        except FileNotFoundError:
            logging.info("prescriptions.json not found, creating new file")
            return []
        except Exception as e:
            logging.error(f"Error loading prescriptions: {e}")
            return []
    
    def _save_prescriptions(self):
        """Sauvegarde les ordonnances dans le fichier JSON."""
        try:
            data = [prescription.to_dict() for prescription in self.prescriptions]
            self.storage_manager.save_data('prescriptions.json', data)
            logging.info("Successfully saved prescriptions.json")
            return True
        except Exception as e:
            logging.error(f"Error saving prescriptions: {e}")
            return False
    
    def create_prescription(self, patient_id, doctor_id, medications, instructions=""):
        """Crée une nouvelle ordonnance."""
        try:
            prescription = Prescription(patient_id, doctor_id, medications, instructions)
            self.prescriptions.append(prescription)
            
            if self._save_prescriptions():
                return True, f"Ordonnance {prescription.prescription_id} créée avec succès"
            else:
                return False, "Erreur lors de la sauvegarde de l'ordonnance"
        except Exception as e:
            logging.error(f"Error creating prescription: {e}")
            return False, f"Erreur lors de la création: {str(e)}"
    
    def get_prescriptions_for_patient(self, patient_id):
        """Récupère toutes les ordonnances d'un patient."""
        return [p for p in self.prescriptions if p.patient_id == patient_id]
    
    def get_prescriptions_for_doctor(self, doctor_id):
        """Récupère toutes les ordonnances d'un médecin."""
        return [p for p in self.prescriptions if p.doctor_id == doctor_id]
    
    def get_prescription_by_id(self, prescription_id):
        """Récupère une ordonnance par son ID."""
        for prescription in self.prescriptions:
            if prescription.prescription_id == prescription_id:
                return prescription
        return None
    
    def delete_prescription(self, prescription_id):
        """Supprime une ordonnance."""
        prescription = self.get_prescription_by_id(prescription_id)
        if prescription:
            self.prescriptions.remove(prescription)
            if self._save_prescriptions():
                return True, f"Ordonnance {prescription_id} supprimée avec succès"
            else:
                return False, "Erreur lors de la suppression"
        return False, "Ordonnance non trouvée"
    
    def update_prescription(self, prescription_id, medications=None, instructions=None):
        """Met à jour une ordonnance existante."""
        prescription = self.get_prescription_by_id(prescription_id)
        if prescription:
            if medications is not None:
                prescription.medications = medications
            if instructions is not None:
                prescription.instructions = instructions
            
            if self._save_prescriptions():
                return True, f"Ordonnance {prescription_id} mise à jour avec succès"
            else:
                return False, "Erreur lors de la mise à jour"
        return False, "Ordonnance non trouvée"
    
    def get_all_prescriptions(self):
        """Récupère toutes les ordonnances."""
        return self.prescriptions 