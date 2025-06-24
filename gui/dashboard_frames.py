import tkinter as tk
from tkinter import ttk, messagebox
from managers.appointment_manager import AppointmentManager
from managers.storage_manager import StorageManager
from managers.user_manager import UserManager
from managers.schedule_manager import ScheduleManager
from managers.prescription_manager import PrescriptionManager
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
import logging

# --- Base Frame for Content ---
class ContentFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='white')

# --- Patient Frames ---
class PatientDashboardFrame(ContentFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        label = ttk.Label(self, text=f"Bienvenue, {controller.user['first_name']} !", font=('Helvetica', 18, 'bold'))
        label.pack(pady=20, padx=20)

        summary_label = ttk.Label(self, text="Voici un résumé de vos prochains rendez-vous et notifications.", font=('Helvetica', 12))
        summary_label.pack(pady=10, padx=20)

class PatientAppointmentsFrame(ContentFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.appointment_manager = AppointmentManager(StorageManager())
        self.user_manager = UserManager(StorageManager())
        
        # --- Main Layout ---
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ttk.Label(self, text="Mes Rendez-vous", font=('Helvetica', 18, 'bold'))
        header.grid(row=0, column=0, pady=20, padx=20, sticky='w')

        # --- Frame for Existing Appointments ---
        appointments_frame = ttk.LabelFrame(self, text="Mes Rendez-vous", padding=10)
        appointments_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)

        # Create Treeview for appointments
        columns = ("ID", "Médecin", "Date", "Heure", "Statut", "Raison")
        self.appointments_tree = ttk.Treeview(appointments_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(appointments_frame, orient='vertical', command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointments_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Action buttons frame
        actions_frame = ttk.Frame(self)
        actions_frame.grid(row=2, column=0, pady=20, sticky='ew', padx=20)
        
        cancel_button = ttk.Button(actions_frame, text="Annuler le Rendez-vous Sélectionné", 
                                  command=self.cancel_selected_appointment)
        cancel_button.pack(side='left', padx=10)
        
        refresh_button = ttk.Button(actions_frame, text="Actualiser", 
                                   command=self.load_patient_appointments)
        refresh_button.pack(side='right', padx=10)

        self.load_patient_appointments()

    def load_patient_appointments(self):
        # Toujours recharger les rendez-vous depuis le fichier
        self.appointment_manager.appointments = self.appointment_manager._load_appointments()
        for i in self.appointments_tree.get_children():
            self.appointments_tree.delete(i)
        
        patient_id = self.controller.user['patient_id']
        appointments = self.appointment_manager.get_appointments_for_patient(patient_id)
        
        doctors = {user['doctor_id']: f"{user['first_name']} {user['last_name']}" 
                   for user in self.user_manager.users if user['role'] == 'Doctor'}

        for app in sorted(appointments, key=lambda x: x['start_time'], reverse=True):
            doctor_name = doctors.get(app['doctor_id'], "Inconnu")
            start_time = datetime.fromisoformat(app['start_time'])
            
            self.appointments_tree.insert("", "end", values=(
                app['appointment_id'],
                doctor_name,
                start_time.strftime('%Y-%m-%d'),
                start_time.strftime('%H:%M'),
                app['status'],
                app['reason']
            ))

    def cancel_selected_appointment(self):
        selected_item = self.appointments_tree.selection()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un rendez-vous à annuler.")
            return
        
        appointment_id = self.appointments_tree.item(selected_item[0])['values'][0]
        
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir annuler ce rendez-vous ?"):
            success, message = self.appointment_manager.cancel_appointment(appointment_id)
            if success:
                messagebox.showinfo("Succès", message)
                self.load_patient_appointments()
            else:
                messagebox.showerror("Erreur", message)

class PatientNewAppointmentFrame(ContentFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.appointment_manager = AppointmentManager(StorageManager())
        self.user_manager = UserManager(StorageManager())
        self.schedule_manager = ScheduleManager(StorageManager())
        self.doctors_by_specialty = self._get_doctors_by_specialty()
        
        # --- Main Layout ---
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        header = ttk.Label(self, text="Prendre un Nouveau Rendez-vous", font=('Helvetica', 18, 'bold'))
        header.grid(row=0, column=0, pady=20, padx=20, sticky='w')

        # --- Frame for Booking ---
        booking_frame = ttk.LabelFrame(self, text="Formulaire de Prise de Rendez-vous", padding=20)
        booking_frame.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)
        booking_frame.grid_columnconfigure(1, weight=1)

        # Specialty
        ttk.Label(booking_frame, text="Spécialité:", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=10)
        self.specialty_var = tk.StringVar()
        self.specialty_cb = ttk.Combobox(booking_frame, textvariable=self.specialty_var, 
                                        values=list(self.doctors_by_specialty.keys()), 
                                        state="readonly", width=30)
        self.specialty_cb.grid(row=0, column=1, sticky="ew", padx=5, pady=10)
        self.specialty_cb.bind("<<ComboboxSelected>>", self.update_doctor_options)

        # Doctor
        ttk.Label(booking_frame, text="Médecin:", font=('Helvetica', 12, 'bold')).grid(row=1, column=0, sticky="w", padx=5, pady=10)
        self.doctor_var = tk.StringVar()
        self.doctor_cb = ttk.Combobox(booking_frame, textvariable=self.doctor_var, 
                                     state="readonly", width=30)
        self.doctor_cb.grid(row=1, column=1, sticky="ew", padx=5, pady=10)

        # Date
        ttk.Label(booking_frame, text="Date:", font=('Helvetica', 12, 'bold')).grid(row=2, column=0, sticky="w", padx=5, pady=10)
        self.date_entry = DateEntry(booking_frame, date_pattern='y-mm-dd', width=30)
        self.date_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=10)

        # Show Available Slots Button
        show_slots_button = ttk.Button(booking_frame, text="Afficher Créneaux Disponibles", 
                                      command=self.show_available_slots)
        show_slots_button.grid(row=3, column=1, sticky="e", padx=5, pady=10)
        
        # Available Slots
        ttk.Label(booking_frame, text="Heures Disponibles:", font=('Helvetica', 12, 'bold')).grid(row=4, column=0, sticky="w", padx=5, pady=10)
        self.slots_listbox = tk.Listbox(booking_frame, height=8, width=30)
        self.slots_listbox.grid(row=4, column=1, sticky="ew", padx=5, pady=10)

        # Reason
        ttk.Label(booking_frame, text="Raison de la visite:", font=('Helvetica', 12, 'bold')).grid(row=5, column=0, sticky="w", padx=5, pady=10)
        self.reason_entry = ttk.Entry(booking_frame, width=30)
        self.reason_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=10)

        # Book Button
        book_button = ttk.Button(booking_frame, text="Prendre Rendez-vous", 
                                command=self.book_appointment, style='Accent.TButton')
        book_button.grid(row=6, column=1, sticky="e", padx=5, pady=20)

    def _get_doctors_by_specialty(self):
        doctors = [user for user in self.user_manager.users if user['role'] == 'Doctor']
        specialties = {}
        for doc in doctors:
            spec = doc['specialty']
            if spec not in specialties:
                specialties[spec] = []
            specialties[spec].append( (f"{doc['first_name']} {doc['last_name']}", doc['doctor_id']) )
        return specialties

    def update_doctor_options(self, event):
        selected_specialty = self.specialty_var.get()
        doctor_names = [name for name, id in self.doctors_by_specialty.get(selected_specialty, [])]
        self.doctor_cb['values'] = doctor_names
        if doctor_names:
            self.doctor_cb.set(doctor_names[0])

    def show_available_slots(self):
        self.slots_listbox.delete(0, tk.END)
        doctor_name = self.doctor_var.get()
        selected_date = self.date_entry.get_date()
        
        if not doctor_name or not selected_date:
            messagebox.showerror("Erreur", "Veuillez sélectionner un médecin et une date.")
            return

        doctor_id = None
        for spec, docs in self.doctors_by_specialty.items():
            for name, id in docs:
                if name == doctor_name:
                    doctor_id = id
                    break
        
        if not doctor_id:
            messagebox.showerror("Erreur", "Impossible de trouver le médecin sélectionné.")
            return
            
        available_slots = self.schedule_manager.get_doctor_availability(doctor_id)
        
        for slot in available_slots:
            start_time = datetime.fromisoformat(slot['start_time'])
            slot_date = start_time.date()
            
            if slot_date == selected_date:
                self.slots_listbox.insert(tk.END, start_time.strftime('%H:%M'))
        
        if self.slots_listbox.size() == 0:
            all_slots = self.schedule_manager.get_doctor_schedule(doctor_id)
            available_dates = set()
            for slot in all_slots:
                if not slot['is_reserved']:
                    slot_date = datetime.fromisoformat(slot['start_time']).date()
                    available_dates.add(slot_date)
            
            if available_dates:
                dates_str = ", ".join([d.strftime('%Y-%m-%d') for d in sorted(available_dates)[:5]])
                messagebox.showinfo("Aucun créneau pour la date sélectionnée", 
                                  f"Aucun créneau disponible pour {selected_date}.\n\nDates disponibles pour ce médecin: {dates_str}")
            else:
                messagebox.showinfo("Aucun créneau", "Aucun créneau disponible trouvé pour ce médecin.")

    def book_appointment(self):
        doctor_name = self.doctor_var.get()
        selected_date = self.date_entry.get_date()
        selected_time_str = self.slots_listbox.get(tk.ACTIVE)
        reason = self.reason_entry.get()
        
        if not self.controller.user or 'patient_id' not in self.controller.user:
            messagebox.showerror("Erreur", "Utilisateur non connecté ou ID patient manquant.")
            return
        patient_id = self.controller.user['patient_id']

        if not all([doctor_name, selected_date, selected_time_str, reason]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs et sélectionner un créneau horaire.")
            return

        doctor_id = None
        for spec, docs in self.doctors_by_specialty.items():
            for name, id in docs:
                if name == doctor_name:
                    doctor_id = id
                    break
        
        if not doctor_id:
            messagebox.showerror("Erreur", "Médecin non trouvé.")
            return

        hour, minute = map(int, selected_time_str.split(':'))
        start_time = datetime(selected_date.year, selected_date.month, selected_date.day, hour, minute)
        end_time = start_time + timedelta(hours=1)
        
        try:
            success, message = self.appointment_manager.book_appointment(patient_id, doctor_id, start_time, end_time, reason, auto_confirm=True)
            if success:
                messagebox.showinfo("Succès", message)
                self.controller.show_content("PatientAppointmentsFrame")
            else:
                messagebox.showerror("Erreur", message)
        except Exception as e:
            logging.error(f"Exception in book_appointment: {e}")
            messagebox.showerror("Erreur", "Une erreur inattendue est survenue.")

class PatientProfileFrame(ContentFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.user_manager = UserManager(StorageManager())
        self.user_info = self.user_manager.find_user_by_email(controller.user['email'])

        frame = ttk.Frame(self, padding="20")
        frame.pack(expand=True, fill="both")
        
        ttk.Label(frame, text="Mon Profil", font=('Helvetica', 18, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        fields = ["first_name", "last_name", "email", "phone", "date_of_birth", "social_security_number"]
        labels = ["Prénom", "Nom", "Email", "Téléphone", "Date de Naissance", "Numéro de Sécurité Sociale"]
        
        self.entries = {}
        for i, field in enumerate(fields):
            ttk.Label(frame, text=labels[i] + ":").grid(row=i+1, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(frame, font=('Helvetica', 11))
            entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=5)
            if self.user_info:
                entry.insert(0, self.user_info.get(field, ''))
            # Seule la date de naissance est en lecture seule
            if field == 'date_of_birth':
                entry.config(state='readonly')
            self.entries[field] = entry
        
        frame.columnconfigure(1, weight=1)

        save_button = ttk.Button(frame, text="Enregistrer les modifications", command=self.save_profile)
        save_button.grid(row=len(fields)+1, column=1, sticky="e", pady=20)

    def save_profile(self):
        # Assurer que l'email de l'utilisateur actuel est disponible
        if not self.controller.user or 'email' not in self.controller.user:
            messagebox.showerror("Erreur", "Impossible d'identifier l'utilisateur actuel.")
            return

        current_email = self.controller.user['email']
        updated_data = {field: entry.get() for field, entry in self.entries.items()}
        
        # Validation du numéro de téléphone (exactement 10 chiffres)
        phone = updated_data.get('phone', '').strip()
        if phone:
            phone_digits = ''.join(filter(str.isdigit, phone))
            if len(phone_digits) != 10:
                messagebox.showerror("Erreur", "Le numéro de téléphone doit contenir exactement 10 chiffres.")
                return
            updated_data['phone'] = phone_digits
        
        # Validation de l'email
        email = updated_data.get('email', '').strip()
        if not email or '@' not in email:
            messagebox.showerror("Erreur", "L'adresse email n'est pas valide.")
            return
        
        # Utiliser l'email actuel pour la mise à jour
        if self.user_manager.update_user(current_email, updated_data):
            # Mettre à jour les informations dans le contrôleur si l'email n'a pas changé
            if self.controller.user and current_email == updated_data['email']:
                self.controller.user.update(updated_data)
            
            messagebox.showinfo("Mise à jour du profil", "Vos informations ont été mises à jour avec succès.")
            
            # Si l'email a été changé, demander à l'utilisateur de se reconnecter
            if current_email != updated_data['email']:
                messagebox.showinfo("Reconnexion requise", "Votre email a été modifié. Veuillez vous reconnecter.")
                self.controller.logout()
        else:
            messagebox.showerror("Erreur", "La mise à jour du profil a échoué.")

# --- Doctor Frames ---
class DoctorDashboardFrame(ContentFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.appointment_manager = AppointmentManager(StorageManager())
        self.schedule_manager = ScheduleManager(StorageManager())
        self.user_manager = UserManager(StorageManager())
        self.prescription_manager = PrescriptionManager(StorageManager())
        self.doctor_id = controller.user['doctor_id']
        
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill='x', pady=(0, 20))
        
        doctor_name = f"Dr. {controller.user['first_name']} {controller.user['last_name']}"
        specialty = controller.user.get('specialty', 'General Medicine')
        
        ttk.Label(header_frame, text=doctor_name, font=('Helvetica', 24, 'bold')).pack(anchor='w')
        ttk.Label(header_frame, text=f"Specialty: {specialty}", font=('Helvetica', 14), foreground='gray').pack(anchor='w')
        
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)
        
        self.appointments_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.appointments_frame, text="Mes Rendez-vous")
        self.setup_appointments_tab()
        
        self.schedule_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.schedule_frame, text="Gérer Planning")
        self.setup_schedule_tab()
        
        self.prescriptions_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.prescriptions_frame, text="Ordonnances")
        self.setup_prescriptions_tab()
        
        self.load_doctor_appointments()
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
    def on_tab_changed(self, event):
        current_tab = self.notebook.select()
        tab_id = self.notebook.index(current_tab)
        
        if tab_id == 0:
            self.load_doctor_appointments()
        elif tab_id == 1:
            self.load_doctor_schedule()
        elif tab_id == 2:
            self.load_doctor_prescriptions()
    
    def refresh_dashboard(self):
        try:
            self.load_doctor_appointments()
            self.load_doctor_schedule()
            self.load_doctor_prescriptions()
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")
            import traceback
            traceback.print_exc()
        
    def setup_appointments_tab(self):
        controls_frame = ttk.Frame(self.appointments_frame)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(controls_frame, text="Filtrer par statut:").pack(side='left', padx=(0, 10))
        self.status_filter = tk.StringVar(value="Tous")
        status_cb = ttk.Combobox(controls_frame, textvariable=self.status_filter, 
                                values=["Tous", "Planifié", "Terminé", "Annulé"], width=15)
        status_cb.pack(side='left', padx=(0, 10))
        status_cb.bind("<<ComboboxSelected>>", lambda e: self.load_doctor_appointments())
        
        refresh_btn = ttk.Button(controls_frame, text="Actualiser", command=self.load_doctor_appointments)
        refresh_btn.pack(side='right')
        
        columns = ("ID", "Patient", "Date", "Heure", "Statut", "Raison")
        self.appointments_tree = ttk.Treeview(self.appointments_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(self.appointments_frame, orient='vertical', command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointments_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        actions_frame = ttk.Frame(self.appointments_frame)
        actions_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(actions_frame, text="Marquer comme Terminé", command=self.mark_appointment_completed).pack(side='left', padx=(0, 10))
        ttk.Button(actions_frame, text="Voir Détails", command=self.view_appointment_details).pack(side='left')
        
    def setup_schedule_tab(self):
        add_frame = ttk.LabelFrame(self.schedule_frame, text="Ajouter Disponibilité", padding=10)
        add_frame.pack(fill='x', pady=(0, 20))
        
        date_frame = ttk.Frame(add_frame)
        date_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(date_frame, text="Date:").pack(side='left')
        self.schedule_date = DateEntry(date_frame, date_pattern='y-mm-dd')
        self.schedule_date.pack(side='left', padx=(10, 0))
        
        time_frame = ttk.Frame(add_frame)
        time_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(time_frame, text="Heure de début:").pack(side='left')
        self.start_hour = tk.StringVar(value="09")
        self.start_minute = tk.StringVar(value="00")
        ttk.Spinbox(time_frame, from_=0, to=23, width=5, textvariable=self.start_hour).pack(side='left', padx=(10, 5))
        ttk.Label(time_frame, text=":").pack(side='left')
        ttk.Spinbox(time_frame, from_=0, to=59, width=5, textvariable=self.start_minute).pack(side='left', padx=(5, 10))
        
        ttk.Label(time_frame, text="Heure de fin:").pack(side='left', padx=(20, 0))
        self.end_hour = tk.StringVar(value="17")
        self.end_minute = tk.StringVar(value="00")
        ttk.Spinbox(time_frame, from_=0, to=23, width=5, textvariable=self.end_hour).pack(side='left', padx=(10, 5))
        ttk.Label(time_frame, text=":").pack(side='left')
        ttk.Spinbox(time_frame, from_=0, to=59, width=5, textvariable=self.end_minute).pack(side='left', padx=(5, 0))
        
        ttk.Button(add_frame, text="Ajouter Disponibilité", command=self.add_availability).pack(pady=(10, 0))
        
        block_frame = ttk.LabelFrame(self.schedule_frame, text="Bloquer Créneaux (Marquer comme Indisponible)", padding=10)
        block_frame.pack(fill='x', pady=(0, 20))
        
        block_date_frame = ttk.Frame(block_frame)
        block_date_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(block_date_frame, text="Date:").pack(side='left')
        self.block_date = DateEntry(block_date_frame, date_pattern='y-mm-dd')
        self.block_date.pack(side='left', padx=(10, 0))
        
        block_time_frame = ttk.Frame(block_frame)
        block_time_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(block_time_frame, text="Heure de début:").pack(side='left')
        self.block_start_hour = tk.StringVar(value="12")
        self.block_start_minute = tk.StringVar(value="00")
        ttk.Spinbox(block_time_frame, from_=0, to=23, width=5, textvariable=self.block_start_hour).pack(side='left', padx=(10, 5))
        ttk.Label(block_time_frame, text=":").pack(side='left')
        ttk.Spinbox(block_time_frame, from_=0, to=59, width=5, textvariable=self.block_start_minute).pack(side='left', padx=(5, 10))
        
        ttk.Label(block_time_frame, text="Heure de fin:").pack(side='left', padx=(20, 0))
        self.block_end_hour = tk.StringVar(value="13")
        self.block_end_minute = tk.StringVar(value="00")
        ttk.Spinbox(block_time_frame, from_=0, to=23, width=5, textvariable=self.block_end_hour).pack(side='left', padx=(10, 5))
        ttk.Label(block_time_frame, text=":").pack(side='left')
        ttk.Spinbox(block_time_frame, from_=0, to=59, width=5, textvariable=self.block_end_minute).pack(side='left', padx=(5, 0))
        
        ttk.Button(block_frame, text="Bloquer Créneaux", command=self.block_time_slots).pack(pady=(10, 0))
        
        schedule_display_frame = ttk.LabelFrame(self.schedule_frame, text="Planning Actuel", padding=10)
        schedule_display_frame.pack(fill='both', expand=True)
        
        schedule_columns = ("Date", "Heure Début", "Heure Fin", "Statut")
        self.schedule_tree = ttk.Treeview(schedule_display_frame, columns=schedule_columns, show='headings', height=10)
        
        for col in schedule_columns:
            self.schedule_tree.heading(col, text=col)
            self.schedule_tree.column(col, width=120)
        
        schedule_scrollbar = ttk.Scrollbar(schedule_display_frame, orient='vertical', command=self.schedule_tree.yview)
        self.schedule_tree.configure(yscrollcommand=schedule_scrollbar.set)
        
        self.schedule_tree.pack(side='left', fill='both', expand=True)
        schedule_scrollbar.pack(side='right', fill='y')
        
        schedule_actions_frame = ttk.Frame(schedule_display_frame)
        schedule_actions_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(schedule_actions_frame, text="Bloquer Sélectionné", command=self.block_selected_slot).pack(side='left', padx=(0, 10))
        ttk.Button(schedule_actions_frame, text="Débloquer Sélectionné", command=self.unblock_selected_slot).pack(side='left', padx=(0, 10))
        ttk.Button(schedule_actions_frame, text="Actualiser Planning", command=self.load_doctor_schedule).pack(side='left')
        
        self.load_doctor_schedule()
        
    def setup_prescriptions_tab(self):
        """Configure l'onglet des ordonnances."""
        # Frame principal avec scrollbar
        main_frame = ttk.Frame(self.prescriptions_frame)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame pour créer une nouvelle ordonnance
        create_frame = ttk.LabelFrame(main_frame, text="Nouvelle Ordonnance", padding=10)
        create_frame.pack(fill='x', pady=(0, 10))
        
        # Sélection du patient
        patient_frame = ttk.Frame(create_frame)
        patient_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(patient_frame, text="Patient:").pack(side='left', padx=(0, 10))
        self.patient_var = tk.StringVar()
        patients = [u for u in self.user_manager.users if u['role'] == 'Patient']
        patient_names = [f"{p['first_name']} {p['last_name']} ({p['email']})" for p in patients]
        
        self.patient_combo = ttk.Combobox(patient_frame, textvariable=self.patient_var, 
                                         values=patient_names, state="readonly", width=40)
        self.patient_combo.pack(side='left', fill='x', expand=True)
        
        # Frame pour les médicaments
        meds_frame = ttk.LabelFrame(create_frame, text="Médicaments", padding=10)
        meds_frame.pack(fill='x', pady=(0, 10))
        
        # Entrées pour un médicament
        med_entry_frame = ttk.Frame(meds_frame)
        med_entry_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(med_entry_frame, text="Nom:").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.med_name_entry = ttk.Entry(med_entry_frame, width=20)
        self.med_name_entry.grid(row=0, column=1, padx=(0, 10))
        
        ttk.Label(med_entry_frame, text="Dosage:").grid(row=0, column=2, sticky='w', padx=(0, 5))
        self.med_dosage_entry = ttk.Entry(med_entry_frame, width=15)
        self.med_dosage_entry.grid(row=0, column=3, padx=(0, 10))
        
        ttk.Label(med_entry_frame, text="Fréquence:").grid(row=0, column=4, sticky='w', padx=(0, 5))
        self.med_frequency_entry = ttk.Entry(med_entry_frame, width=15)
        self.med_frequency_entry.grid(row=0, column=5, padx=(0, 10))
        
        ttk.Label(med_entry_frame, text="Durée:").grid(row=0, column=6, sticky='w', padx=(0, 5))
        self.med_duration_entry = ttk.Entry(med_entry_frame, width=15)
        self.med_duration_entry.grid(row=0, column=7, padx=(0, 10))
        
        # Bouton pour ajouter un médicament
        add_med_btn = ttk.Button(med_entry_frame, text="+ Ajouter Médicament", 
                                command=self.add_medication_to_list)
        add_med_btn.grid(row=0, column=8, padx=(10, 0))
        
        # Liste des médicaments ajoutés
        self.medications_listbox = tk.Listbox(meds_frame, height=5, width=80)
        self.medications_listbox.pack(fill='x', pady=(0, 5))
        
        # Bouton pour supprimer un médicament
        remove_med_btn = ttk.Button(meds_frame, text="Supprimer Médicament Sélectionné", 
                                   command=self.remove_selected_medication)
        remove_med_btn.pack(anchor='w')
        
        # Instructions générales
        instructions_frame = ttk.Frame(create_frame)
        instructions_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(instructions_frame, text="Instructions générales:").pack(anchor='w')
        self.instructions_text = tk.Text(instructions_frame, height=3, width=80)
        self.instructions_text.pack(fill='x')
        
        # Boutons d'action
        buttons_frame = ttk.Frame(create_frame)
        buttons_frame.pack(fill='x', pady=(10, 0))
        
        create_btn = ttk.Button(buttons_frame, text="Créer Ordonnance", 
                               command=self.create_prescription)
        create_btn.pack(side='left', padx=(0, 10))
        
        clear_btn = ttk.Button(buttons_frame, text="Effacer Formulaire", 
                              command=self.clear_prescription_form)
        clear_btn.pack(side='left')
        
        # Frame pour la liste des ordonnances
        list_frame = ttk.LabelFrame(main_frame, text="Ordonnances Existantes", padding=10)
        list_frame.pack(fill='both', expand=True)
        
        # Contrôles pour la liste
        controls_frame = ttk.Frame(list_frame)
        controls_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(controls_frame, text="Filtrer par patient:").pack(side='left', padx=(0, 10))
        self.prescription_filter = tk.StringVar(value="Tous")
        filter_combo = ttk.Combobox(controls_frame, textvariable=self.prescription_filter, 
                                   values=["Tous"] + patient_names, state="readonly", width=30)
        filter_combo.pack(side='left', padx=(0, 10))
        filter_combo.bind("<<ComboboxSelected>>", lambda e: self.load_doctor_prescriptions())
        
        refresh_btn = ttk.Button(controls_frame, text="Actualiser", 
                                command=self.load_doctor_prescriptions)
        refresh_btn.pack(side='right')
        
        # Treeview pour les ordonnances
        columns = ("ID", "Patient", "Date", "Médicaments", "Instructions")
        self.prescriptions_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            self.prescriptions_tree.heading(col, text=col)
            self.prescriptions_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.prescriptions_tree.yview)
        self.prescriptions_tree.configure(yscrollcommand=scrollbar.set)
        
        self.prescriptions_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Boutons d'action pour les ordonnances
        action_frame = ttk.Frame(list_frame)
        action_frame.pack(fill='x', pady=(10, 0))
        
        ttk.Button(action_frame, text="Voir Détails", 
                  command=self.view_prescription_details).pack(side='left', padx=(0, 10))
        ttk.Button(action_frame, text="Supprimer", 
                  command=self.delete_prescription).pack(side='left')
        
        # Variables pour stocker les médicaments temporaires
        self.temp_medications = []

    def load_doctor_appointments(self):
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        appointments = self.appointment_manager.get_appointments_for_doctor(self.doctor_id)
        
        patients = {user['patient_id']: f"{user['first_name']} {user['last_name']}" 
                   for user in self.user_manager.users if user['role'] == 'Patient'}
        
        status_filter = self.status_filter.get()
        
        for app in appointments:
            if status_filter != "Tous" and app['status'] != status_filter:
                continue
                
            patient_name = patients.get(app['patient_id'], f"Patient {app['patient_id']}")
            start_time = datetime.fromisoformat(app['start_time'])
            
            self.appointments_tree.insert("", "end", values=(
                app['appointment_id'],
                patient_name,
                start_time.strftime('%Y-%m-%d'),
                start_time.strftime('%H:%M'),
                app['status'],
                app['reason']
            ))
    
    def load_doctor_schedule(self):
        for item in self.schedule_tree.get_children():
            self.schedule_tree.delete(item)
        
        schedule = self.schedule_manager.get_doctor_schedule(self.doctor_id)
        
        for slot in schedule:
            start_time = datetime.fromisoformat(slot['start_time'])
            end_time = datetime.fromisoformat(slot['end_time'])
            status = "Réservé" if slot['is_reserved'] else "Disponible"
            
            self.schedule_tree.insert("", "end", values=(
                start_time.strftime('%Y-%m-%d'),
                start_time.strftime('%H:%M'),
                end_time.strftime('%H:%M'),
                status
            ))
    
    def load_doctor_prescriptions(self):
        """Charge la liste des ordonnances du médecin."""
        for item in self.prescriptions_tree.get_children():
            self.prescriptions_tree.delete(item)
        
        prescriptions = self.prescription_manager.get_prescriptions_for_doctor(self.doctor_id)
        patients = {user['patient_id']: f"{user['first_name']} {user['last_name']}" 
                   for user in self.user_manager.users if user['role'] == 'Patient'}
        
        filter_value = self.prescription_filter.get()
        
        for prescription in prescriptions:
            # Filtrer par patient si nécessaire
            patient_name = patients.get(prescription.patient_id, f"Patient {prescription.patient_id}")
            if filter_value != "Tous" and patient_name not in filter_value:
                continue
            
            # Correction : afficher tous les noms de médicaments ou 'Aucun'
            if not prescription.medications:
                meds_text = "Aucun"
            else:
                noms = [med['name'] for med in prescription.medications]
                meds_text = ', '.join(noms)
            
            # Tronquer les instructions si trop longues
            instructions = prescription.instructions[:50] + "..." if len(prescription.instructions) > 50 else prescription.instructions
            
            self.prescriptions_tree.insert('', 'end', values=(
                prescription.prescription_id,
                patient_name,
                prescription.get_formatted_date(),
                meds_text,
                instructions
            ))
    
    def add_medication_to_list(self):
        """Ajoute un médicament à la liste temporaire."""
        name = self.med_name_entry.get().strip()
        dosage = self.med_dosage_entry.get().strip()
        frequency = self.med_frequency_entry.get().strip()
        duration = self.med_duration_entry.get().strip()
        
        if not all([name, dosage, frequency, duration]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs du médicament.")
            return
        
        medication = {
            'name': name,
            'dosage': dosage,
            'frequency': frequency,
            'duration': duration,
            'notes': ""
        }
        
        self.temp_medications.append(medication)
        self.medications_listbox.insert(tk.END, f"{name} - {dosage} - {frequency} - {duration}")
        
        # Vider les champs
        self.med_name_entry.delete(0, tk.END)
        self.med_dosage_entry.delete(0, tk.END)
        self.med_frequency_entry.delete(0, tk.END)
        self.med_duration_entry.delete(0, tk.END)
    
    def remove_selected_medication(self):
        """Supprime le médicament sélectionné de la liste."""
        selection = self.medications_listbox.curselection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un médicament à supprimer.")
            return
        
        index = selection[0]
        self.medications_listbox.delete(index)
        del self.temp_medications[index]
    
    def create_prescription(self):
        """Crée une nouvelle ordonnance."""
        # Vérifier qu'un patient est sélectionné
        patient_selection = self.patient_var.get()
        if not patient_selection:
            messagebox.showerror("Erreur", "Veuillez sélectionner un patient.")
            return
        
        # Extraire l'email du patient depuis la sélection
        patient_email = patient_selection.split('(')[-1].rstrip(')')
        patient = self.user_manager.find_user_by_email(patient_email)
        if not patient:
            messagebox.showerror("Erreur", "Patient non trouvé.")
            return
        
        # Vérifier qu'il y a au moins un médicament
        if not self.temp_medications:
            messagebox.showerror("Erreur", "Veuillez ajouter au moins un médicament.")
            return
        
        # Récupérer les instructions
        instructions = self.instructions_text.get("1.0", tk.END).strip()
        
        # Créer l'ordonnance
        success, message = self.prescription_manager.create_prescription(
            patient['patient_id'], 
            self.doctor_id, 
            list(self.temp_medications),  # copie de la liste !
            instructions
        )
        
        if success:
            messagebox.showinfo("Succès", message)
            self.clear_prescription_form()
            self.load_doctor_prescriptions()
        else:
            messagebox.showerror("Erreur", message)
    
    def clear_prescription_form(self):
        """Efface le formulaire d'ordonnance."""
        self.patient_var.set("")
        self.med_name_entry.delete(0, tk.END)
        self.med_dosage_entry.delete(0, tk.END)
        self.med_frequency_entry.delete(0, tk.END)
        self.med_duration_entry.delete(0, tk.END)
        self.medications_listbox.delete(0, tk.END)
        self.instructions_text.delete("1.0", tk.END)
        self.temp_medications.clear()
    
    def view_prescription_details(self):
        """Affiche les détails d'une ordonnance."""
        selection = self.prescriptions_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner une ordonnance.")
            return
        
        prescription_id = self.prescriptions_tree.item(selection[0])['values'][0]
        prescription = self.prescription_manager.get_prescription_by_id(prescription_id)
        
        if not prescription:
            messagebox.showerror("Erreur", "Ordonnance non trouvée.")
            return
        
        # Créer une fenêtre de détails
        details_window = tk.Toplevel(self)
        details_window.title(f"Détails Ordonnance {prescription_id}")
        details_window.geometry("600x500")
        
        # Récupérer les informations du patient
        patient = self.user_manager.find_user_by_role_id(prescription.patient_id)
        patient_name = f"{patient['first_name']} {patient['last_name']}" if patient else f"Patient {prescription.patient_id}"
        
        # Contenu de la fenêtre
        main_frame = ttk.Frame(details_window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Titre
        ttk.Label(main_frame, text=f"Ordonnance {prescription_id}", 
                 font=('Helvetica', 16, 'bold')).pack(pady=(0, 20))
        
        # Informations générales
        info_frame = ttk.LabelFrame(main_frame, text="Informations générales", padding=10)
        info_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(info_frame, text=f"Patient: {patient_name}").pack(anchor='w')
        ttk.Label(info_frame, text=f"Date: {prescription.get_formatted_date()}").pack(anchor='w')
        
        # Médicaments
        meds_frame = ttk.LabelFrame(main_frame, text="Médicaments", padding=10)
        meds_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Treeview pour les médicaments
        med_columns = ("Nom", "Dosage", "Fréquence", "Durée", "Notes")
        med_tree = ttk.Treeview(meds_frame, columns=med_columns, show='headings', height=8)
        
        for col in med_columns:
            med_tree.heading(col, text=col)
            med_tree.column(col, width=100)
        
        for med in prescription.medications:
            med_tree.insert('', 'end', values=(
                med['name'],
                med['dosage'],
                med['frequency'],
                med['duration'],
                med.get('notes', '')
            ))
        
        med_tree.pack(fill='both', expand=True)
        
        # Instructions
        if prescription.instructions:
            instructions_frame = ttk.LabelFrame(main_frame, text="Instructions générales", padding=10)
            instructions_frame.pack(fill='x')
            
            instructions_text = tk.Text(instructions_frame, height=4, wrap='word')
            instructions_text.insert("1.0", prescription.instructions)
            instructions_text.config(state='disabled')
            instructions_text.pack(fill='x')
    
    def delete_prescription(self):
        """Supprime une ordonnance."""
        selection = self.prescriptions_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner une ordonnance.")
            return
        
        prescription_id = self.prescriptions_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette ordonnance ?\nCette action ne peut pas être annulée."):
            success, message = self.prescription_manager.delete_prescription(prescription_id)
            
            if success:
                messagebox.showinfo("Succès", message)
                self.load_doctor_prescriptions()
            else:
                messagebox.showerror("Erreur", message)

    def mark_appointment_completed(self):
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner un rendez-vous à marquer comme terminé.")
            return
        
        appointment_id = self.appointments_tree.item(selected[0])['values'][0]
        
        for app in self.appointment_manager.appointments:
            if app['appointment_id'] == appointment_id:
                if app['status'] == 'Planifié':
                    app['status'] = 'Terminé'
                    self.appointment_manager._save_appointments()
                    messagebox.showinfo("Succès", f"Rendez-vous {appointment_id} marqué comme terminé.")
                    self.load_doctor_appointments()
                else:
                    messagebox.showwarning("Attention", f"Le rendez-vous {appointment_id} est déjà {app['status']}.")
                return
        
        messagebox.showerror("Erreur", "Rendez-vous introuvable.")
    
    def view_appointment_details(self):
        selected = self.appointments_tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner un rendez-vous pour voir les détails.")
            return
        
        values = self.appointments_tree.item(selected[0])['values']
        appointment_id = values[0]
        
        for app in self.appointment_manager.appointments:
            if app['appointment_id'] == appointment_id:
                start_time = datetime.fromisoformat(app['start_time'])
                end_time = datetime.fromisoformat(app['end_time'])
                
                details = f"""Détails du Rendez-vous:
                
ID: {app['appointment_id']}
ID Patient: {app['patient_id']}
Date: {start_time.strftime('%Y-%m-%d')}
Heure: {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}
Statut: {app['status']}
Raison: {app['reason']}"""
                
                messagebox.showinfo("Détails du Rendez-vous", details)
                return
        
        messagebox.showerror("Erreur", "Rendez-vous introuvable.")
    
    def add_availability(self):
        try:
            selected_date = self.schedule_date.get_date()
            start_hour = int(self.start_hour.get())
            start_minute = int(self.start_minute.get())
            end_hour = int(self.end_hour.get())
            end_minute = int(self.end_minute.get())
            
            if start_hour < 0 or start_hour > 23 or end_hour < 0 or end_hour > 23:
                raise ValueError("Les heures doivent être entre 0 et 23")
            if start_minute < 0 or start_minute > 59 or end_minute < 0 or end_minute > 59:
                raise ValueError("Les minutes doivent être entre 0 et 59")
            
            start_time = datetime(selected_date.year, selected_date.month, selected_date.day, start_hour, start_minute)
            end_time = datetime(selected_date.year, selected_date.month, selected_date.day, end_hour, end_minute)
            
            if start_time >= end_time:
                messagebox.showerror("Erreur", "L'heure de début doit être avant l'heure de fin.")
                return
            
            current_time = start_time
            slots_added = 0
            
            while current_time < end_time:
                slot_end = current_time + timedelta(hours=1)
                if slot_end <= end_time:
                    result = self.schedule_manager.add_availability(self.doctor_id, current_time, slot_end)
                    if result:
                        slots_added += 1
                current_time = slot_end
            
            messagebox.showinfo("Succès", f"Ajouté {slots_added} créneaux de disponibilité pour {selected_date.strftime('%Y-%m-%d')}.")
            self.load_doctor_schedule()
            
        except ValueError as e:
            messagebox.showerror("Erreur", f"Format d'heure invalide: {e}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec de l'ajout de disponibilité: {e}")

    def block_time_slots(self):
        try:
            selected_date = self.block_date.get_date()
            start_hour = int(self.block_start_hour.get())
            start_minute = int(self.block_start_minute.get())
            end_hour = int(self.block_end_hour.get())
            end_minute = int(self.block_end_minute.get())
            
            if start_hour < 0 or start_hour > 23 or end_hour < 0 or end_hour > 23:
                raise ValueError("Les heures doivent être entre 0 et 23")
            if start_minute < 0 or start_minute > 59 or end_minute < 0 or end_minute > 59:
                raise ValueError("Les minutes doivent être entre 0 et 59")
            
            start_time = datetime(selected_date.year, selected_date.month, selected_date.day, start_hour, start_minute)
            end_time = datetime(selected_date.year, selected_date.month, selected_date.day, end_hour, end_minute)
            
            if start_time >= end_time:
                messagebox.showerror("Erreur", "L'heure de début doit être avant l'heure de fin.")
                return
            
            current_time = start_time
            slots_blocked = 0
            
            while current_time < end_time:
                slot_end = current_time + timedelta(hours=1)
                if slot_end <= end_time:
                    if self.schedule_manager.block_timeslot(self.doctor_id, current_time, slot_end):
                        slots_blocked += 1
                current_time = slot_end
            
            if slots_blocked > 0:
                messagebox.showinfo("Succès", f"Bloqué {slots_blocked} créneaux pour {selected_date.strftime('%Y-%m-%d')}.")
                self.load_doctor_schedule()
            else:
                messagebox.showwarning("Attention", "Aucun créneau n'a été bloqué. Ils peuvent déjà être bloqués ou réservés.")
            
        except ValueError as e:
            messagebox.showerror("Erreur", f"Format d'heure invalide: {e}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Échec du blocage des créneaux: {e}")

    def unblock_selected_slot(self):
        selected = self.schedule_tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner un créneau à débloquer.")
            return
        
        values = self.schedule_tree.item(selected[0])['values']
        date_str = values[0]
        start_time_str = values[1]
        
        schedule = self.schedule_manager.get_doctor_schedule(self.doctor_id)
        for slot in schedule:
            start_time = datetime.fromisoformat(slot['start_time'])
            if (start_time.strftime('%Y-%m-%d') == date_str and 
                start_time.strftime('%H:%M') == start_time_str):
                
                if slot['is_reserved']: 
                    if self.schedule_manager.unblock_timeslot(self.doctor_id, slot['start_time']):
                        messagebox.showinfo("Succès", f"Débloqué le créneau {start_time_str} du {date_str}.")
                        self.load_doctor_schedule()
                    else:
                        messagebox.showerror("Erreur", "Échec du déblocage du créneau.")
                else:
                    messagebox.showinfo("Information", "Ce créneau est déjà disponible.")
                return
        
        messagebox.showerror("Erreur", "Créneau sélectionné introuvable dans le planning.")

    def block_selected_slot(self):
        selected = self.schedule_tree.selection()
        if not selected:
            messagebox.showerror("Erreur", "Veuillez sélectionner un créneau à bloquer.")
            return
        
        values = self.schedule_tree.item(selected[0])['values']
        date_str = values[0]
        start_time_str = values[1]
        
        schedule = self.schedule_manager.get_doctor_schedule(self.doctor_id)
        for slot in schedule:
            start_time = datetime.fromisoformat(slot['start_time'])
            if (start_time.strftime('%Y-%m-%d') == date_str and 
                start_time.strftime('%H:%M') == start_time_str):
                
                if not slot['is_reserved']:
                    if self.schedule_manager.block_timeslot(self.doctor_id, start_time, start_time + timedelta(hours=1)):
                        messagebox.showinfo("Succès", f"Créneau {start_time_str} du {date_str} bloqué avec succès.")
                        self.load_doctor_schedule()
                    else:
                        messagebox.showerror("Erreur", "Échec du blocage du créneau.")
                else:
                    messagebox.showinfo("Info", "Ce créneau est déjà bloqué ou un rendez-vous est planifié.")
                return
        
        messagebox.showerror("Erreur", "Créneau sélectionné introuvable dans le planning.")

    def refresh_all_data(self):
        try:
            print("Refreshing all doctor dashboard data...")
            self.load_doctor_appointments()
            self.load_doctor_schedule()
            self.load_doctor_prescriptions()
            messagebox.showinfo("Succès", "Données du tableau de bord actualisées avec succès.")
        except Exception as e:
            print(f"Error refreshing dashboard: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erreur", f"Échec de l'actualisation des données: {e}")

# --- Secretary Frames ---
class SecretaryDashboardFrame(tk.Frame):
    def __init__(self, parent, main_app):
        tk.Frame.__init__(self, parent)
        self.main_app = main_app
        self.configure(bg='#1a1a2e')
        
        # Initialize managers
        self.user_manager = UserManager(StorageManager())
        self.appointment_manager = AppointmentManager(StorageManager())
        
        # Load and display Yoda background image
        self.setup_yoda_background()
        
        # Title
        title_label = tk.Label(self, text="Tableau de Bord - Secrétariat", 
                              font=('Helvetica', 18, 'bold'), 
                              bg='#1a1a2e', fg='#ffd700')
        title_label.pack(pady=20)
        
        # Welcome message
        welcome_text = f"Bienvenue, {self.main_app.user['first_name']} {self.main_app.user['last_name']}"
        welcome_label = tk.Label(self, text=welcome_text, 
                                 font=('Helvetica', 14), 
                                 bg='#1a1a2e', fg='white')
        welcome_label.pack(pady=10)
        
        # Quick actions frame
        actions_frame = tk.Frame(self, bg='#1a1a2e')
        actions_frame.pack(pady=20, fill='x', padx=20)
        
        actions_title = tk.Label(actions_frame, text="Actions Rapides", 
                                 font=('Helvetica', 16, 'bold'), 
                                 bg='#1a1a2e', fg='#ffd700')
        actions_title.pack(pady=10)
        
        # Action buttons
        actions = [
            ("📅 Gérer Rendez-vous", self.show_appointments_management),
            ("👥 Liste Patients", self.show_patients_list),
            ("👨‍⚕️ Liste Médecins", self.show_doctors_list),
            ("➕ Nouveau Rendez-vous", self.show_new_appointment),
            ("➕ Nouveau Patient", self.open_new_patient_window)
        ]
        
        for text, command in actions:
            btn = tk.Button(actions_frame, text=text, 
                           font=('Helvetica', 12, 'bold'),
                           bg='#ffd700', fg='#1a1a2e',
                           command=command, width=25, height=2)
            btn.pack(pady=5)

    def setup_yoda_background(self):
        """Configure l'image Yoda en arrière-plan avec transparence."""
        try:
            yoda_path = os.path.join("assets", "yoda.png")
            if os.path.exists(yoda_path):
                original_image = Image.open(yoda_path)
                window_width = 400
                window_height = 400
                img_width, img_height = original_image.size
                scale = min(window_width / img_width, window_height / img_height) * 0.7
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.yoda_photo = ImageTk.PhotoImage(resized_image)
                # Place Yoda image tout au fond
                self.yoda_label = tk.Label(self, image=self.yoda_photo, bg='#1a1a2e', borderwidth=0, highlightthickness=0)
                self.yoda_label.place(relx=0.5, rely=0.85, anchor='center')
                self.yoda_label.lower() # S'assurer que l'image est en arrière-plan
        except Exception as e:
            print(f"Erreur lors du chargement de l'image Yoda: {e}")

    def show_appointments_management(self):
        """Affiche la gestion des rendez-vous."""
        self.main_app.show_content("Appointments Management")

    def show_patients_list(self):
        """Affiche la liste des patients."""
        self.main_app.show_content("Patients List")

    def show_doctors_list(self):
        """Affiche la liste des médecins."""
        self.main_app.show_content("Doctors List")

    def show_new_appointment(self):
        """Affiche le formulaire de nouveau rendez-vous."""
        self.main_app.show_content("New Appointment")

    def open_new_patient_window(self):
        win = tk.Toplevel(self)
        win.title("Nouveau Patient")
        win.geometry("400x400")
        win.configure(bg='#1a1a2e')
        
        labels = ["Prénom", "Nom", "Email", "Téléphone", "Date de naissance (YYYY-MM-DD)", "Registre National", "Mot de passe"]
        entries = []
        for i, label in enumerate(labels):
            tk.Label(win, text=label, bg='#1a1a2e', fg='white', font=('Helvetica', 12)).pack(pady=5)
            entry = tk.Entry(win, font=('Helvetica', 12))
            entry.pack(pady=2)
            entries.append(entry)
        
        def create_patient():
            first_name = entries[0].get()
            last_name = entries[1].get()
            email = entries[2].get()
            phone = entries[3].get()
            dob = entries[4].get()
            ssn = entries[5].get()
            password = entries[6].get()
            if not all([first_name, last_name, email, phone, dob, ssn, password]):
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")
                return
            result = self.user_manager.register_patient(first_name, last_name, email, phone, password, dob, ssn)
            if result:
                messagebox.showinfo("Succès", "Patient créé avec succès !")
                win.destroy()
                # Actualiser la liste des patients si elle est affichée
                if hasattr(self.main_app, 'frames') and 'Patients List' in self.main_app.frames:
                    self.main_app.frames['Patients List'].load_patients()
            else:
                messagebox.showerror("Erreur", "Erreur lors de la création du patient.")
        
        tk.Button(win, text="Créer", command=create_patient, font=('Helvetica', 12, 'bold'), bg='#44ff44', fg='#1a1a2e').pack(pady=20)

class SecretaryAppointmentsFrame(tk.Frame):
    def __init__(self, parent, main_app):
        tk.Frame.__init__(self, parent)
        self.main_app = main_app
        self.configure(bg='#1a1a2e')
        
        # Initialize managers
        self.user_manager = UserManager(StorageManager())
        self.appointment_manager = AppointmentManager(StorageManager())
        
        # Title
        title_label = tk.Label(self, text="Gestion des Rendez-vous", 
                              font=('Helvetica', 18, 'bold'), 
                              bg='#1a1a2e', fg='#ffd700')
        title_label.pack(pady=20)
        
        # Filter frame
        filter_frame = tk.Frame(self, bg='#1a1a2e')
        filter_frame.pack(pady=10, fill='x', padx=20)
        
        tk.Label(filter_frame, text="Filtrer par statut:", 
                font=('Helvetica', 12), bg='#1a1a2e', fg='white').pack(side='left', padx=5)
        
        self.status_var = tk.StringVar(value="all")
        status_combo = ttk.Combobox(filter_frame, textvariable=self.status_var, 
                                   values=["all", "pending", "planned", "cancelled"], 
                                   state="readonly", width=15)
        status_combo.pack(side='left', padx=5)
        status_combo.bind('<<ComboboxSelected>>', self.refresh_appointments)
        
        # Refresh button
        refresh_btn = tk.Button(filter_frame, text="🔄 Actualiser", 
                               font=('Helvetica', 10, 'bold'),
                               bg='#44ff44', fg='#1a1a2e',
                               command=self.refresh_appointments)
        refresh_btn.pack(side='right', padx=5)
        
        # Appointments list frame
        list_frame = tk.Frame(self, bg='#1a1a2e')
        list_frame.pack(pady=10, fill='both', expand=True, padx=20)
        
        # Create Treeview for appointments
        columns = ('ID', 'Patient', 'Médecin', 'Date', 'Heure', 'Statut', 'Raison')
        self.appointments_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.appointments_tree.heading(col, text=col)
            self.appointments_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        self.appointments_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Action buttons frame
        actions_frame = tk.Frame(self, bg='#1a1a2e')
        actions_frame.pack(pady=20, fill='x', padx=20)
        
        actions = [
            (" Confirmer", self.confirm_appointment, "#44ff44"),
            (" Annuler", self.cancel_appointment, "#ff4444"),
            (" Supprimer", self.delete_appointment, "#ff8800"),
            (" Voir Détails", self.view_appointment_details, "#4444ff"),
            (" Nouveau RDV", self.create_new_appointment, "#ffd700")
        ]
        
        for text, command, color in actions:
            btn = tk.Button(actions_frame, text=text, 
                           font=('Helvetica', 12, 'bold'),
                           bg=color, fg='#1a1a2e',
                           command=command, width=15, height=2)
            btn.pack(side='left', padx=10)
        
        # Load appointments
        self.refresh_appointments()

    def refresh_appointments(self, event=None):
        """Actualise la liste des rendez-vous."""
        # Reload users data to ensure we have the latest
        self.user_manager.users = self.user_manager._load_users()
        self.appointment_manager.appointments = self.appointment_manager._load_appointments()
        
        # Clear existing items
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        # Get appointments
        appointments = self.appointment_manager.get_all_appointments()
        status_filter = self.status_var.get()
        
        # Filter by status if needed
        if status_filter != "all":
            appointments = [a for a in appointments if a['status'] == status_filter]
        
        # Add appointments to treeview
        for appointment in appointments:
            # Get patient and doctor names using role IDs
            patient = self.user_manager.find_user_by_role_id(appointment['patient_id'])
            doctor = self.user_manager.find_user_by_role_id(appointment['doctor_id'])
            
            patient_name = f"{patient['first_name']} {patient['last_name']}" if patient else "Inconnu"
            doctor_name = f"Dr. {doctor['last_name']}" if doctor else "Inconnu"
            
            # Format date and time
            start_time = datetime.fromisoformat(appointment['start_time'])
            date_str = start_time.strftime("%d/%m/%Y")
            time_str = start_time.strftime("%H:%M")
            
            # Status color mapping
            status_colors = {
                'pending': 'orange',
                'confirmed': 'green',
                'cancelled': 'red'
            }
            
            self.appointments_tree.insert('', 'end', values=(
                appointment['appointment_id'],
                patient_name,
                doctor_name,
                date_str,
                time_str,
                appointment['status'],
                appointment['reason']
            ))

    def confirm_appointment(self):
        """Confirme le rendez-vous sélectionné."""
        selection = self.appointments_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un rendez-vous.")
            return
        
        appointment_id = self.appointments_tree.item(selection[0])['values'][0]
        success, message = self.appointment_manager.validate_appointment(appointment_id)
        
        if success:
            messagebox.showinfo("Succès", message)
            self.refresh_appointments()
        else:
            messagebox.showerror("Erreur", message)

    def cancel_appointment(self):
        """Annule le rendez-vous sélectionné."""
        selection = self.appointments_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un rendez-vous.")
            return
        
        appointment_id = self.appointments_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir annuler ce rendez-vous ?"):
            success, message = self.appointment_manager.cancel_appointment(appointment_id)
            
            if success:
                messagebox.showinfo("Succès", message)
                self.refresh_appointments()
            else:
                messagebox.showerror("Erreur", message)

    def view_appointment_details(self):
        """Affiche les détails du rendez-vous sélectionné."""
        selection = self.appointments_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un rendez-vous.")
            return
        
        appointment_id = self.appointments_tree.item(selection[0])['values'][0]
        self.show_appointment_details_window(appointment_id)

    def create_new_appointment(self):
        """Ouvre le formulaire de création de rendez-vous."""
        self.main_app.show_content("New Appointment")

    def show_appointment_details_window(self, appointment_id):
        """Affiche une fenêtre avec les détails du rendez-vous."""
        # Find appointment
        appointments = self.appointment_manager.get_all_appointments()
        appointment = None
        for app in appointments:
            if app['appointment_id'] == appointment_id:
                appointment = app
                break
        
        if not appointment:
            messagebox.showerror("Erreur", "Rendez-vous non trouvé.")
            return
        
        # Create details window
        details_window = tk.Toplevel(self)
        details_window.title(f"Détails Rendez-vous #{appointment_id}")
        details_window.geometry("500x400")
        details_window.configure(bg='#1a1a2e')
        
        # Get patient and doctor info
        patient = self.user_manager.find_user_by_role_id(appointment['patient_id'])
        doctor = self.user_manager.find_user_by_role_id(appointment['doctor_id'])
        
        # Details content
        details_frame = tk.Frame(details_window, bg='#1a1a2e', padx=20, pady=20)
        details_frame.pack(fill='both', expand=True)
        
        # Title
        tk.Label(details_frame, text=f"Rendez-vous #{appointment_id}", 
                font=('Helvetica', 16, 'bold'), bg='#1a1a2e', fg='#ffd700').pack(pady=10)
        
        # Patient info
        if patient:
            tk.Label(details_frame, text=f"Patient: {patient['first_name']} {patient['last_name']}", 
                    font=('Helvetica', 12), bg='#1a1a2e', fg='white').pack(anchor='w', pady=2)
            tk.Label(details_frame, text=f"Email: {patient['email']}", 
                    font=('Helvetica', 12), bg='#1a1a2e', fg='white').pack(anchor='w', pady=2)
            tk.Label(details_frame, text=f"Téléphone: {patient['phone']}", 
                    font=('Helvetica', 12), bg='#1a1a2e', fg='white').pack(anchor='w', pady=2)
        
        # Doctor info
        if doctor:
            tk.Label(details_frame, text=f"Médecin: Dr. {doctor['last_name']}", 
                    font=('Helvetica', 12), bg='#1a1a2e', fg='white').pack(anchor='w', pady=2)
            tk.Label(details_frame, text=f"Spécialité: {doctor['specialty']}", 
                    font=('Helvetica', 12), bg='#1a1a2e', fg='white').pack(anchor='w', pady=2)
        
        # Appointment details
        start_time = datetime.fromisoformat(appointment['start_time'])
        end_time = datetime.fromisoformat(appointment['end_time'])
        
        tk.Label(details_frame, text=f"Date: {start_time.strftime('%d/%m/%Y')}", 
                font=('Helvetica', 12), bg='#1a1a2e', fg='white').pack(anchor='w', pady=2)
        tk.Label(details_frame, text=f"Heure: {start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}", 
                font=('Helvetica', 12), bg='#1a1a2e', fg='white').pack(anchor='w', pady=2)
        tk.Label(details_frame, text=f"Statut: {appointment['status']}", 
                font=('Helvetica', 12), bg='#1a1a2e', fg='white').pack(anchor='w', pady=2)
        tk.Label(details_frame, text=f"Raison: {appointment['reason']}", 
                font=('Helvetica', 12), bg='#1a1a2e', fg='white').pack(anchor='w', pady=2)

    def delete_appointment(self):
        """Supprime le rendez-vous sélectionné."""
        selection = self.appointments_tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un rendez-vous.")
            return
        
        appointment_id = self.appointments_tree.item(selection[0])['values'][0]
        
        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer définitivement ce rendez-vous ?\nCette action ne peut pas être annulée."):
            success, message = self.appointment_manager.delete_appointment(appointment_id)
            
            if success:
                messagebox.showinfo("Succès", message)
                self.refresh_appointments()
            else:
                messagebox.showerror("Erreur", message)

class SecretaryPatientsFrame(tk.Frame):
    def __init__(self, parent, main_app):
        tk.Frame.__init__(self, parent)
        self.main_app = main_app
        self.configure(bg='#1a1a2e')
        
        # Initialize managers
        self.user_manager = UserManager(StorageManager())
        
        # Title
        title_label = tk.Label(self, text="Liste des Patients", 
                              font=('Helvetica', 18, 'bold'), 
                              bg='#1a1a2e', fg='#ffd700')
        title_label.pack(pady=20)
        
        # Bouton Actualiser
        refresh_btn = tk.Button(self, text="🔄 Actualiser", font=('Helvetica', 10, 'bold'), bg='#44ff44', fg='#1a1a2e', command=self.load_patients)
        refresh_btn.pack(pady=(0, 10))
        
        # Patients list frame
        list_frame = tk.Frame(self, bg='#1a1a2e')
        list_frame.pack(pady=10, fill='both', expand=True, padx=20)
        
        # Create Treeview for patients
        columns = ('ID', 'Nom', 'Prénom', 'Email', 'Téléphone', 'Date Naissance', 'Sécurité Sociale')
        self.patients_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.patients_tree.heading(col, text=col)
            self.patients_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.patients_tree.yview)
        self.patients_tree.configure(yscrollcommand=scrollbar.set)
        
        self.patients_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load patients
        self.load_patients()

    def load_patients(self):
        """Charge la liste des patients."""
        # Recharger les données depuis le fichier
        self.user_manager.users = self.user_manager._load_users()
        
        # Clear existing items
        for item in self.patients_tree.get_children():
            self.patients_tree.delete(item)
        
        # Get patients
        patients = [u for u in self.user_manager.users if u['role'] == 'Patient']
        
        # Add patients to treeview
        for patient in patients:
            self.patients_tree.insert('', 'end', values=(
                patient['patient_id'],
                patient['last_name'],
                patient['first_name'],
                patient['email'],
                patient['phone'],
                patient.get('date_of_birth', 'N/A'),
                patient.get('social_security_number', 'N/A')
            ))

class SecretaryDoctorsFrame(tk.Frame):
    def __init__(self, parent, main_app):
        tk.Frame.__init__(self, parent)
        self.main_app = main_app
        self.configure(bg='#1a1a2e')
        
        # Initialize managers
        self.user_manager = UserManager(StorageManager())
        
        # Title
        title_label = tk.Label(self, text="Liste des Médecins", 
                              font=('Helvetica', 18, 'bold'), 
                              bg='#1a1a2e', fg='#ffd700')
        title_label.pack(pady=20)
        
        # Doctors list frame
        list_frame = tk.Frame(self, bg='#1a1a2e')
        list_frame.pack(pady=10, fill='both', expand=True, padx=20)
        
        # Create Treeview for doctors
        columns = ('ID', 'Nom', 'Prénom', 'Email', 'Téléphone', 'Spécialité')
        self.doctors_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configure columns
        for col in columns:
            self.doctors_tree.heading(col, text=col)
            self.doctors_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.doctors_tree.yview)
        self.doctors_tree.configure(yscrollcommand=scrollbar.set)
        
        self.doctors_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Load doctors
        self.load_doctors()

    def load_doctors(self):
        """Charge la liste des médecins."""
        # Clear existing items
        for item in self.doctors_tree.get_children():
            self.doctors_tree.delete(item)
        
        # Get doctors
        doctors = [u for u in self.user_manager.users if u['role'] == 'Doctor']
        
        # Add doctors to treeview
        for doctor in doctors:
            self.doctors_tree.insert('', 'end', values=(
                doctor['doctor_id'],
                doctor['last_name'],
                doctor['first_name'],
                doctor['email'],
                doctor['phone'],
                doctor.get('specialty', 'N/A')
            ))

class SecretaryNewAppointmentFrame(tk.Frame):
    def __init__(self, parent, main_app):
        tk.Frame.__init__(self, parent)
        self.main_app = main_app
        self.configure(bg='#1a1a2e')
        
        # Initialize managers
        self.user_manager = UserManager(StorageManager())
        self.appointment_manager = AppointmentManager(StorageManager())
        
        # Title
        title_label = tk.Label(self, text="Nouveau Rendez-vous", 
                              font=('Helvetica', 18, 'bold'), 
                              bg='#1a1a2e', fg='#ffd700')
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = tk.Frame(self, bg='#1a1a2e')
        form_frame.pack(pady=20, padx=20)
        
        # Patient selection
        tk.Label(form_frame, text="Patient:", 
                font=('Helvetica', 12), bg='#1a1a2e', fg='white').grid(row=0, column=0, sticky='w', pady=5)
        
        self.patient_var = tk.StringVar()
        patients = [u for u in self.user_manager.users if u['role'] == 'Patient']
        patient_names = [f"{p['first_name']} {p['last_name']} ({p['email']})" for p in patients]
        
        self.patient_combo = ttk.Combobox(form_frame, textvariable=self.patient_var, 
                                         values=patient_names, state="readonly", width=40)
        self.patient_combo.grid(row=0, column=1, sticky='ew', pady=5, padx=10)
        
        # Doctor selection
        tk.Label(form_frame, text="Médecin:", 
                font=('Helvetica', 12), bg='#1a1a2e', fg='white').grid(row=1, column=0, sticky='w', pady=5)
        
        self.doctor_var = tk.StringVar()
        doctors = [u for u in self.user_manager.users if u['role'] == 'Doctor']
        doctor_names = [f"Dr. {d['last_name']} - {d['specialty']}" for d in doctors]
        
        self.doctor_combo = ttk.Combobox(form_frame, textvariable=self.doctor_var, 
                                        values=doctor_names, state="readonly", width=40)
        self.doctor_combo.grid(row=1, column=1, sticky='ew', pady=5, padx=10)
        
        # Date selection
        tk.Label(form_frame, text="Date:", 
                font=('Helvetica', 12), bg='#1a1a2e', fg='white').grid(row=2, column=0, sticky='w', pady=5)
        
        self.date_entry = tk.Entry(form_frame, font=('Helvetica', 12), width=20)
        self.date_entry.grid(row=2, column=1, sticky='ew', pady=5, padx=10)
        self.date_entry.insert(0, "YYYY-MM-DD")
        
        # Time selection
        tk.Label(form_frame, text="Heure:", 
                font=('Helvetica', 12), bg='#1a1a2e', fg='white').grid(row=3, column=0, sticky='w', pady=5)
        
        self.time_entry = tk.Entry(form_frame, font=('Helvetica', 12), width=20)
        self.time_entry.grid(row=3, column=1, sticky='ew', pady=5, padx=10)
        self.time_entry.insert(0, "HH:MM")
        
        # Reason
        tk.Label(form_frame, text="Raison:", 
                font=('Helvetica', 12), bg='#1a1a2e', fg='white').grid(row=4, column=0, sticky='w', pady=5)
        
        self.reason_entry = tk.Entry(form_frame, font=('Helvetica', 12), width=40)
        self.reason_entry.grid(row=4, column=1, sticky='ew', pady=5, padx=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(self, bg='#1a1a2e')
        buttons_frame.pack(pady=20)
        
        # Create button
        create_btn = tk.Button(buttons_frame, text="Créer Rendez-vous", 
                              font=('Helvetica', 12, 'bold'),
                              bg='#44ff44', fg='#1a1a2e',
                              command=self.create_appointment, width=20, height=2)
        create_btn.pack(side='left', padx=10)
        
        # Cancel button
        cancel_btn = tk.Button(buttons_frame, text="Annuler", 
                              font=('Helvetica', 12, 'bold'),
                              bg='#ff4444', fg='#1a1a2e',
                              command=lambda: self.main_app.show_content("Dashboard"), 
                              width=20, height=2)
        cancel_btn.pack(side='left', padx=10)

    def create_appointment(self):
        """Crée un nouveau rendez-vous."""
        try:
            # Get selected patient
            patient_selection = self.patient_var.get()
            if not patient_selection:
                messagebox.showerror("Erreur", "Veuillez sélectionner un patient.")
                return
            
            patient_email = patient_selection.split('(')[-1].rstrip(')')
            patient = self.user_manager.find_user_by_email(patient_email)
            if not patient:
                messagebox.showerror("Erreur", "Patient non trouvé.")
                return
            
            # Get selected doctor
            doctor_selection = self.doctor_var.get()
            if not doctor_selection:
                messagebox.showerror("Erreur", "Veuillez sélectionner un médecin.")
                return
            
            doctor_name = doctor_selection.split(' - ')[0].replace('Dr. ', '')
            doctor = None
            for d in self.user_manager.users:
                if d['role'] == 'Doctor' and d['last_name'] == doctor_name:
                    doctor = d
                    break
            
            if not doctor:
                messagebox.showerror("Erreur", "Médecin non trouvé.")
                return
            
            # Get date and time
            date_str = self.date_entry.get()
            time_str = self.time_entry.get()
            
            if date_str == "YYYY-MM-DD" or time_str == "HH:MM":
                messagebox.showerror("Erreur", "Veuillez saisir une date et heure valides.")
                return
            
            # Create datetime
            datetime_str = f"{date_str}T{time_str}:00"
            start_time = datetime.fromisoformat(datetime_str)
            end_time = start_time + timedelta(hours=1)
            
            # Get reason
            reason = self.reason_entry.get()
            if not reason:
                messagebox.showerror("Erreur", "Veuillez saisir une raison.")
                return
            
            # Create appointment
            success, message = self.appointment_manager.book_appointment(
                patient['patient_id'], doctor['doctor_id'], start_time, end_time, reason, auto_confirm=False
            )
            
            if success:
                messagebox.showinfo("Succès", message)
                self.main_app.show_content("PatientAppointmentsFrame")
            else:
                messagebox.showerror("Erreur", message)
                
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la création: {str(e)}")

