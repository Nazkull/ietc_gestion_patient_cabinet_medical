import json
from datetime import datetime, timedelta, Patient, Medecin

class RDV:
    def __init__(self, rdv_id, patient, medecin, date_heure, duree_minutes):
        self.rdv_id = rdv_id
        self.patient = patient
        self.medecin = medecin
        self.date_heure = date_heure
        self.duree_minutes = duree_minutes
    def to_dict(self):
        return{"rdv_id":self.rdv_id,
               "patient":{"id": self.patient.patient_id,
                         "nom": self.patient.nom,
                         "prenom": self.patient.prenom
                         },
                "medecin":{"id": self.medecin.medecin_id,
                           "nom": self.medecin.nom,
                           "specialite": self.medecin.specialite
                          },
                "date_heure": self.date_heure.isoformat(),
                "duree_minutes": self.duree_minutes
              }
class GestionnaireRDV:
    def __init__(self, fichier="rdv.json"):
        self.rdv = []
        self.fichier = fichier
        self.charger_fichier()
                
    def disponibilite(self, medecin, date_heure, duree):
        for rdv in self.rdv:
            if rdv.medecin.medecin_id == medecin.medecin_id:
                debut = rdv.date_heure
                fin = debut + timedelta(minutes=rdv.duree_minutes)
                nouveau_debut = date_heure
                nouveau_fin = nouveau_debut + timedelta(minutes=duree)

                if debut < nouveau_fin and nouveau_debut < fin:
                    return False
        return True

    def ajouter_rdv(self, rdv):
        if self.disponibilite(rdv.medecin, rdv.date_heure, rdv.duree_minutes):
            self.rdv.append(rdv)
            self.sauvegarde()
            print("Rendez-vous confirmé.")
        else:
            print("Date non disponible.")

    def lister_rdv(self):
        for rdv in self.rdv:
            print(f"{rdv.date_heure} - {rdv.patient.nom} avec Dr. {rdv.medecin.nom}")
    def sauvegarde(self):
        data=[rdv.to_dict() for rdv in self.rdv]
        with open(self.fichier,"w") as f:
            json.dump(data, f, indent=4)
                    
