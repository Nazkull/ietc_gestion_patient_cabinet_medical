import tkinter as tk
from tkinter import ttk, messagebox
import logging
from managers.email_manager import EmailManager
from managers.reminder_manager import ReminderManager

class EmailConfigFrame(ttk.Frame):
    def __init__(self, parent, main_app):
        super().__init__(parent)
        self.main_app = main_app
        self.reminder_manager = main_app.appointment_manager.reminder_manager
        self.email_manager = EmailManager()
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Titre
        title_label = ttk.Label(self, text="Rappel", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # Frame principal
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Instructions
        instructions = ttk.Label(
            main_frame, 
            text="Configuration Gmail pour l'envoi de rappels automatiques",
            font=("Arial", 10),
            wraplength=400
        )
        instructions.pack(pady=10)
        
        # Configuration Gmail
        gmail_frame = ttk.LabelFrame(main_frame, text="Configuration Gmail", padding=15)
        gmail_frame.pack(fill="x", pady=10)
        
        # Email Gmail
        ttk.Label(gmail_frame, text="Email Gmail:").pack(anchor="w")
        self.gmail_email_entry = ttk.Entry(gmail_frame, width=40)
        self.gmail_email_entry.pack(fill="x", pady=5)
        
        # Mot de passe Gmail
        ttk.Label(gmail_frame, text="Mot de passe Gmail:").pack(anchor="w", pady=(10,0))
        self.gmail_password_entry = ttk.Entry(gmail_frame, width=40, show="*")
        self.gmail_password_entry.pack(fill="x", pady=5)
        
        # Status
        self.status_label = ttk.Label(main_frame, text="", font=("Arial", 9))
        self.status_label.pack(pady=10)
        
        # Charger la configuration existante
        self.load_existing_config()
        
        # Boutons d'action
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        # Bouton pour envoyer les rappels de demain
        send_reminders_btn = ttk.Button(
            button_frame, 
            text="Envoyer les rappels pour demain", 
            command=self.send_tomorrow_reminders,
            style="Action.TButton"
        )
        send_reminders_btn.pack(side="left", padx=5, pady=10)
        
        # Bouton de sauvegarde
        save_btn = ttk.Button(
            button_frame, 
            text="Sauvegarder la configuration", 
            command=self.save_configuration,
            style="Action.TButton"
        )
        save_btn.pack(side="left", padx=5, pady=10)
        
    def load_existing_config(self):
        """Charge la configuration existante dans les champs"""
        if self.email_manager.is_configured:
            self.gmail_email_entry.insert(0, self.email_manager.sender_email or "")
            self.gmail_password_entry.insert(0, self.email_manager.sender_password or "")
            self.status_label.config(text="✅ Configuration chargée", foreground="green")
        
    def save_configuration(self):
        """Sauvegarde la configuration email"""
        try:
            email = self.gmail_email_entry.get().strip()
            password = self.gmail_password_entry.get().strip()
            
            if not email or not password:
                messagebox.showwarning("Champs requis", "Veuillez remplir tous les champs.")
                return
                
            # Configurer l'email manager
            self.email_manager.configure(email, password)
            
            # Configurer le reminder manager
            self.reminder_manager.email_manager = self.email_manager
            
            messagebox.showinfo("Succès", "Configuration sauvegardée avec succès !")
            self.status_label.config(text="✅ Configuration sauvegardée", foreground="green")
            
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {str(e)}")
            self.status_label.config(text="❌ Erreur de sauvegarde", foreground="red")
            
    def send_tomorrow_reminders(self):
        """Envoie manuellement les rappels pour les rendez-vous de demain"""
        try:
            # Vérifier si l'email est configuré
            if not self.email_manager.is_configured:
                messagebox.showwarning("Configuration requise", 
                                     "Veuillez d'abord configurer l'email avant d'envoyer des rappels.")
                return
                
            # Envoyer les rappels
            result = self.reminder_manager.send_manual_reminders_for_tomorrow()
            
            if result["success"]:
                if result['count'] > 0:
                    messagebox.showinfo("Rappels envoyés", 
                                      f"Rappels envoyés avec succès !\n\n{result['message']}\n\n"
                                      f"Nombre de rappels envoyés: {result['count']}")
                    self.status_label.config(text=f"✅ {result['count']} rappels envoyés", foreground="green")
                else:
                    messagebox.showinfo("Information", "Aucun rappel à envoyer pour demain.")
                    self.status_label.config(text="ℹ️ Aucun rappel à envoyer", foreground="blue")
            else:
                messagebox.showerror("Erreur d'envoi",
                                   f"Impossible d'envoyer les rappels.\n\n"
                                   f"Détail : {result['message']}")
                self.status_label.config(text=f"❌ Échec de l'envoi des rappels", foreground="red")

        except Exception as e:
            logging.error(f"Erreur lors de l'envoi manuel des rappels: {e}")
            messagebox.showerror("Erreur Critique", f"Une erreur critique est survenue: {e}")
            self.status_label.config(text="❌ Erreur critique", foreground="red") 