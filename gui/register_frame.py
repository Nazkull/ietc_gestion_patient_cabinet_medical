import tkinter as tk
from tkinter import ttk, messagebox
from managers.user_manager import UserManager
from managers.storage_manager import StorageManager
import re
from datetime import datetime

class RegisterFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_manager = UserManager(StorageManager())

        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TButton', font=('Helvetica', 12, 'bold'))
        style.configure('Header.TLabel', font=('Helvetica', 24, 'bold'))

        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        header_label = ttk.Label(main_frame, text="Créer un nouveau compte", style='Header.TLabel')
        header_label.grid(row=0, column=0, columnspan=2, pady=20)

        # --- Form Fields ---
        ttk.Label(main_frame, text="Prénom :").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.first_name_entry = ttk.Entry(main_frame, width=40)
        self.first_name_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Nom :").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.last_name_entry = ttk.Entry(main_frame, width=40)
        self.last_name_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Email :").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = ttk.Entry(main_frame, width=40)
        self.email_entry.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        
        ttk.Label(main_frame, text="Téléphone :").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.phone_entry = ttk.Entry(main_frame, width=40)
        self.phone_entry.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Numéro de sécurité sociale :").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.ssn_entry = ttk.Entry(main_frame, width=40)
        self.ssn_entry.grid(row=5, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Date de naissance (YYYY-MM-DD) :").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.dob_entry = ttk.Entry(main_frame, width=40)
        self.dob_entry.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

        ttk.Label(main_frame, text="Mot de passe :").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = ttk.Entry(main_frame, show="*", width=40)
        self.password_entry.grid(row=7, column=1, sticky="ew", padx=5, pady=5)

        # --- Buttons ---
        register_button = ttk.Button(main_frame, text="Créer le compte", command=self.register)
        register_button.grid(row=8, column=1, sticky="e", pady=20)

        back_button = ttk.Button(main_frame, text="Retour à la connexion", command=lambda: self.controller.show_login_frame())
        back_button.grid(row=8, column=0, sticky="w", pady=20)

    def _validate_email(self, email):
        """Validates email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _validate_phone(self, phone):
        """Validates phone number format: exactly 10 digits."""
        clean_phone = re.sub(r'[^\d]', '', phone)
        return len(clean_phone) == 10

    def _validate_ssn(self, ssn):
        """Validates social security number format."""
        clean_ssn = re.sub(r'[^\d]', '', ssn)
        return len(clean_ssn) >= 10

    def _validate_date(self, date_str):
        """Validates date format."""
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def _validate_password(self, password):
        """Validates password strength."""
        return len(password) >= 6

    def _clear_fields(self):
        """Clears all input fields."""
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        if hasattr(self, 'dob_entry'):
            self.dob_entry.delete(0, tk.END)
        if hasattr(self, 'ssn_entry'):
            self.ssn_entry.delete(0, tk.END)

    def show_forgot_password(self):
        messagebox.showinfo("Mot de passe oublié", "Veuillez envoyer un mail au secrétariat : secretary@clinic.com")

    def register(self):
        """Handles the registration process with validation."""
        # Get basic fields
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        ssn = self.ssn_entry.get().strip()
        dob = self.dob_entry.get().strip()
        password = self.password_entry.get().strip()
        # Basic validation
        if not all([first_name, last_name, email, phone, password, dob, ssn]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs obligatoires.")
            return
        if not self._validate_email(email):
            messagebox.showerror("Erreur", "Format d'email invalide.")
            self.email_entry.focus()
            return
        if not self._validate_phone(phone):
            messagebox.showerror("Erreur", "Le numéro de téléphone doit contenir exactement 10 chiffres.")
            self.phone_entry.focus()
            return
        if not self._validate_password(password):
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 6 caractères.")
            self.password_entry.focus()
            return
        if not self._validate_date(dob):
            messagebox.showerror("Erreur", "Format de date invalide (YYYY-MM-DD).")
            self.dob_entry.focus()
            return
        if not self._validate_ssn(ssn):
            messagebox.showerror("Erreur", "Format de numéro de sécurité sociale invalide.")
            self.ssn_entry.focus()
            return
        user = self.user_manager.register_patient(
            first_name, last_name, email, phone, password, dob, ssn
        )
        if user:
            messagebox.showinfo("Succès", f"Compte créé avec succès ! Bienvenue, {first_name} !")
            self._clear_fields()
        else:
            messagebox.showerror("Erreur", "Erreur lors de la création du compte.") 