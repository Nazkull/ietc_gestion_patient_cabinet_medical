import tkinter as tk
from tkinter import ttk

class SidebarFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='#1a1a2e')
        self.controller = controller
        self.buttons = {}

    def create_buttons(self, button_config):
        # Clear old buttons
        for widget in self.winfo_children():
            widget.destroy()
        self.buttons = {}
        
        # Create new buttons
        for text, command in button_config.items():
            button = tk.Button(self, text=text, command=command,
                              bg='#ffd700', fg='#1a1a2e', 
                              font=('Helvetica', 12, 'bold'),
                              relief='flat', anchor='w', padx=10)
            button.pack(fill='x', pady=5, padx=5)
            self.buttons[text] = button

    def create_patient_buttons(self):
        buttons = {
            "Tableau de bord": lambda: self.controller.show_content("PatientDashboardFrame"),
            "Prendre RDV": lambda: self.controller.show_content("PatientNewAppointmentFrame"),
            "Mes Rendez-vous": lambda: self.controller.show_content("PatientAppointmentsFrame"),
            "Notifications": lambda: self.controller.show_content("NotificationFrame"),
            "Mon Profil": lambda: self.controller.show_content("PatientProfileFrame"),
            "Déconnexion": self.controller.logout,
        }
        self.create_buttons(buttons)

    def create_doctor_buttons(self):
        buttons = {
            "Tableau de bord": lambda: self.controller.show_content("DoctorDashboardFrame"),
            "Notifications": lambda: self.controller.show_content("NotificationFrame"),
            "Mon Profil": lambda: self.controller.show_content("DoctorProfileFrame"),
            "Déconnexion": self.controller.logout,
        }
        self.create_buttons(buttons)

    def create_secretary_buttons(self):
        buttons = {
            "Tableau de bord": lambda: self.controller.show_content("SecretaryDashboardFrame"),
            "Gérer RDV": lambda: self.controller.show_content("Appointments Management"),
            "Patients": lambda: self.controller.show_content("Patients List"),
            "Médecins": lambda: self.controller.show_content("Doctors List"),
            "Nouveau RDV": lambda: self.controller.show_content("New Appointment"),
            "Nouveau Patient": self.controller.open_new_patient_window,
            "Notifications": lambda: self.controller.show_content("NotificationFrame"),
            "Rappel": lambda: self.controller.show_content("EmailConfigFrame"),
            "Déconnexion": self.controller.logout,
        }
        self.create_buttons(buttons) 