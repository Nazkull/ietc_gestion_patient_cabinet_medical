from tkinter import Tk, StringVar, messagebox, ttk

import customtkinter as ctk

# Configure the main application window
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class MedicalCabinetApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cabinet Médical")
        self.geometry("800x600")

        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Bienvenue au Cabinet Médical", font=("Arial", 24))
        self.title_label.pack(pady=20)

        # Patient Management Section
        self.patient_frame = ctk.CTkFrame(self)
        self.patient_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.patient_label = ctk.CTkLabel(self.patient_frame, text="Gestion des Patients", font=("Arial", 18))
        self.patient_label.pack(pady=10)

        self.add_patient_button = ctk.CTkButton(self.patient_frame, text="Ajouter un Patient", command=self.add_patient)
        self.add_patient_button.pack(pady=5)

        self.view_patient_button = ctk.CTkButton(self.patient_frame, text="Voir les Patients", command=self.view_patients)
        self.view_patient_button.pack(pady=5)

        # Appointment Management Section
        self.appointment_frame = ctk.CTkFrame(self)
        self.appointment_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.appointment_label = ctk.CTkLabel(self.appointment_frame, text="Gestion des Rendez-vous", font=("Arial", 18))
        self.appointment_label.pack(pady=10)

        self.add_appointment_button = ctk.CTkButton(self.appointment_frame, text="Ajouter un Rendez-vous", command=self.add_appointment)
        self.add_appointment_button.pack(pady=5)

        self.view_appointment_button = ctk.CTkButton(self.appointment_frame, text="Voir les Rendez-vous", command=self.view_appointments)
        self.view_appointment_button.pack(pady=5)

    def add_patient(self):
        print("Ajouter un patient - Fonctionnalité à implémenter")

    def view_patients(self):
        print("Voir les patients - Fonctionnalité à implémenter")

    def add_appointment(self):
        print("Ajouter un rendez-vous - Fonctionnalité à implémenter")

    def view_appointments(self):
        print("Voir les rendez-vous - Fonctionnalité à implémenter")

if __name__ == "__main__":
    app = MedicalCabinetApp()
    app.mainloop()