import tkinter as tk
from tkinter import ttk, messagebox
from managers.user_manager import UserManager
from managers.storage_manager import StorageManager
import re

class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.user_manager = UserManager(StorageManager())
        
        # Configure frame with Star Wars colors
        self.configure(bg='#1a1a2e', padx=40, pady=40)
        
        # Title with Star Wars styling
        title_label = tk.Label(self, text="CENTRE MÉDICAL CORUSCANT", 
                              font=('Arial', 24, 'bold'), 
                              fg='#ffd700', bg='#1a1a2e')  # Gold text
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(self, text="Terminal d'Accès aux Services de Santé de la République", 
                                 font=('Arial', 12), 
                                 fg='#87ceeb', bg='#1a1a2e')  # Sky blue text
        subtitle_label.pack(pady=(0, 30))
        
        # Login form
        form_frame = tk.Frame(self, bg='#1a1a2e')
        form_frame.pack()
        
        # Username/ID field
        tk.Label(form_frame, text="Identifiant Citoyen:", 
                font=('Arial', 12, 'bold'), 
                fg='#ffd700', bg='#1a1a2e').pack(anchor='w', pady=(0, 5))
        self.username_entry = tk.Entry(form_frame, font=('Arial', 12), 
                                      bg='#2a2a3e', fg='white', 
                                      insertbackground='#ffd700')  # Gold cursor
        self.username_entry.pack(fill='x', pady=(0, 15))
        
        # Password field
        tk.Label(form_frame, text="Code de Sécurité:", 
                font=('Arial', 12, 'bold'), 
                fg='#ffd700', bg='#1a1a2e').pack(anchor='w', pady=(0, 5))
        self.password_entry = tk.Entry(form_frame, show="*", font=('Arial', 12), 
                                      bg='#2a2a3e', fg='white',
                                      insertbackground='#ffd700')
        self.password_entry.pack(fill='x', pady=(0, 25))
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame, bg='#1a1a2e')
        buttons_frame.pack()
        
        # Largeur commune pour les deux boutons
        button_width = 28
        # Login button with blue styling
        login_button = tk.Button(buttons_frame, text="ACCÉDER AU TERMINAL", 
                                command=self.login,
                                font=('Arial', 12, 'bold'),
                                bg='#4169e1', fg='white',
                                activebackground='#5a7de8', activeforeground='white',
                                relief='raised', bd=3)
        login_button.pack(fill='x', pady=(0, 5))
        
        # Register button
        register_button = tk.Button(buttons_frame, text="NOUVELLE INSCRIPTION CITOYEN", 
                                   command=self.show_register,
                                   font=('Arial', 10, 'bold'),
                                   bg='#4169e1', fg='white',
                                   activebackground='#5a7de8', activeforeground='white',
                                   relief='raised', bd=2)
        register_button.pack(fill='x')
        
        # Mot de passe oublié button (below the two options)
        forgot_pw_button = tk.Button(form_frame, text="Mot de passe oublié ?", 
                                    command=self.forgot_password,
                                    font=('Arial', 10, 'italic'),
                                    bg='#1a1a2e', fg='#87ceeb',
                                    activebackground='#23233a', activeforeground='#ffd700',
                                    relief='flat', bd=0, cursor='hand2')
        forgot_pw_button.pack(pady=(18, 0))
        
        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda event: self.login())
        
        # Focus on username entry
        self.username_entry.focus()

    def _validate_email(self, email):
        """Validates email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _clear_fields(self):
        """Clears the input fields."""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def login(self):
        email = self.username_entry.get()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Échec de Connexion", "L'identifiant citoyen et le code de sécurité sont requis.")
            return

        if not self._validate_email(email):
            messagebox.showerror("Échec de Connexion", "Format d'email invalide.")
            self.username_entry.focus()
            return

        try:
            user = self.user_manager.login_user(email, password)
            if user:
                messagebox.showinfo("Succès", f"Bienvenue, {user['first_name']}!")
                self._clear_fields()
                self.controller.show_dashboard(user)
            else:
                messagebox.showerror("Échec de Connexion", "Identifiant citoyen ou code de sécurité invalide.")
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()
        except Exception as e:
            messagebox.showerror("Échec de Connexion", f"Erreur lors de la connexion: {str(e)}")
            self.password_entry.delete(0, tk.END)

    def show_register(self):
        self.controller.show_register_frame()

    def forgot_password(self):
        messagebox.showinfo("Mot de passe oublié", "Veuillez envoyer un mail au secrétariat à l'adresse secretary@clinic.com pour réinitialiser votre mot de passe.") 