import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from managers.user_manager import UserManager
from managers.storage_manager import StorageManager
from managers.appointment_manager import AppointmentManager
from gui.login_frame import LoginFrame
from gui.register_frame import RegisterFrame
from gui.sidebar_frame import SidebarFrame
from gui.dashboard_frames import (PatientDashboardFrame, PatientAppointmentsFrame, 
                                 PatientNewAppointmentFrame, PatientProfileFrame, 
                                 DoctorDashboardFrame, SecretaryDashboardFrame, 
                                 SecretaryAppointmentsFrame, SecretaryPatientsFrame, 
                                 SecretaryDoctorsFrame, SecretaryNewAppointmentFrame)
from gui.notification_frame import NotificationFrame
from gui.email_config_frame import EmailConfigFrame

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.title("Centre Médical Coruscant - Services de Santé de la République")
        parent.geometry("1024x768")
        
        # Initialize managers
        self.storage_manager = StorageManager()
        self.user_manager = UserManager(self.storage_manager)
        self.appointment_manager = AppointmentManager(self.storage_manager)
        
        # --- Background Image ---
        try:
            bg_image_pil = Image.open("assets/background.png")
            self.bg_image = ImageTk.PhotoImage(bg_image_pil.resize((1024, 768), Image.Resampling.LANCZOS))
            background_label = tk.Label(parent, image=self.bg_image)
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
        except (FileNotFoundError, IOError):
            print("Background image not found. Continuing without it.")
        
        self.parent.grid_rowconfigure(0, weight=1)
        self.parent.grid_columnconfigure(0, weight=1)

        self.user = None
        self.main_frame = None # Will hold the dashboard view
        
        # Container for pre-login frames, now on top of the background
        self.auth_container = tk.Frame(parent, bg='#1a1a2e', bd=2, relief='groove')  # Dark blue background
        self.auth_container.place(relx=0.5, rely=0.5, anchor='center')
 
        self.login_frame = LoginFrame(self.auth_container, self)
        self.login_frame.pack()
                 
        self.register_frame = RegisterFrame(self.auth_container, self)
        # We don't pack this initially, we switch to it.
 
        self.show_login_frame()
 
    def show_login_frame(self):
        """Shows the login frame."""
        self.register_frame.pack_forget()
        self.login_frame.pack()
 
    def show_register_frame(self):
        """Shows the registration frame."""
        self.login_frame.pack_forget()
        self.register_frame.pack()
 
    def show_dashboard(self, user):
        """Hides auth frames and shows the main dashboard."""
        self.user = user
        self.auth_container.place_forget() # Hide the login/register container

        # Create the main dashboard layout
        self.main_frame = tk.Frame(self.parent, bg='#0a0a0a') # Dark background like Star Wars
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        # Make the main frame slightly transparent to see the background
        self.main_frame.config(highlightbackground="#ffd700", highlightthickness=2)  # Gold border like Star Wars
 
        # Create Sidebar
        self.sidebar = SidebarFrame(self.main_frame, self)
        self.sidebar.grid(row=0, column=0, sticky="nsw", padx=(0, 5))
        
        # Create sidebar buttons based on user role
        if self.user['role'] == 'Patient':
            self.sidebar.create_patient_buttons()
        elif self.user['role'] == 'Doctor':
            self.sidebar.create_doctor_buttons()
        elif self.user['role'] == 'Secretary':
            self.sidebar.create_secretary_buttons()
 
        # Create Content Area
        self.content_area = tk.Frame(self.main_frame, bg='#1a1a2e')  # Dark blue background
        self.content_area.grid(row=0, column=1, sticky="nsew")
        self.content_area.grid_rowconfigure(0, weight=1)
        self.content_area.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        # Load frames based on user role
        if self.user['role'] == 'Patient':
            self.frames['PatientDashboardFrame'] = PatientDashboardFrame(self.content_area, self)
            self.frames['PatientAppointmentsFrame'] = PatientAppointmentsFrame(self.content_area, self)
            self.frames['PatientNewAppointmentFrame'] = PatientNewAppointmentFrame(self.content_area, self)
            self.frames['PatientProfileFrame'] = PatientProfileFrame(self.content_area, self)
            self.frames['NotificationFrame'] = NotificationFrame(self.content_area, self)
        elif self.user['role'] == 'Doctor':
            self.frames['DoctorDashboardFrame'] = DoctorDashboardFrame(self.content_area, self)
            self.frames['DoctorProfileFrame'] = PatientProfileFrame(self.content_area, self)  # Réutiliser la frame patient pour le profil
            self.frames['NotificationFrame'] = NotificationFrame(self.content_area, self)
        elif self.user['role'] == 'Secretary':
            self.frames['SecretaryDashboardFrame'] = SecretaryDashboardFrame(self.content_area, self)
            self.frames['Appointments Management'] = SecretaryAppointmentsFrame(self.content_area, self)
            self.frames['Patients List'] = SecretaryPatientsFrame(self.content_area, self)
            self.frames['Doctors List'] = SecretaryDoctorsFrame(self.content_area, self)
            self.frames['New Appointment'] = SecretaryNewAppointmentFrame(self.content_area, self)
            self.frames['NotificationFrame'] = NotificationFrame(self.content_area, self)
            self.frames['EmailConfigFrame'] = EmailConfigFrame(self.content_area, self)
 
        for name, frame in self.frames.items():
            frame.grid(row=0, column=0, sticky="nsew")
 
        # Show the initial dashboard frame
        if self.user['role'] == 'Patient':
            self.show_content("PatientDashboardFrame")
        elif self.user['role'] == 'Doctor':
            self.show_content("DoctorDashboardFrame")
        elif self.user['role'] == 'Secretary':
            self.show_content("SecretaryDashboardFrame")
 
    def show_content(self, content_key):
        """Shows the specified content frame."""
        # Remove temporary frame if it exists
        if hasattr(self, 'temp_frame') and self.temp_frame:
            self.temp_frame.destroy()
            self.temp_frame = None
        
        if content_key in self.frames:
            frame = self.frames[content_key]
            # Show all frames first
            for name, f in self.frames.items():
                f.grid()
            # Then raise the selected one
            frame.tkraise()
        else:
            # Create a temporary frame for pages not yet implemented
            # Don't destroy existing frames, just create a new one
            temp_frame = tk.Frame(self.content_area, bg='white')
            temp_frame.grid(row=0, column=0, sticky="nsew")
            
            # Hide all other frames
            for name, frame in self.frames.items():
                frame.grid_remove()
            
            # Show the temporary frame
            temp_frame.tkraise()
            
            # Add content to temporary frame
            label = ttk.Label(temp_frame, text=f"{content_key} Page - Coming Soon!", font=('Helvetica', 18))
            label.pack(expand=True)
            
            # Store the temp frame so we can remove it later
            self.temp_frame = temp_frame
 
    def logout(self):
        """Logs out and returns to the login screen."""
        self.user = None
        if self.main_frame:
            self.main_frame.destroy()
        self.auth_container.place(relx=0.5, rely=0.5, anchor='center') # Re-show auth container
        self.show_login_frame() 

    def open_new_patient_window(self):
        if hasattr(self, 'frames') and 'SecretaryDashboardFrame' in self.frames:
            self.frames['SecretaryDashboardFrame'].open_new_patient_window() 