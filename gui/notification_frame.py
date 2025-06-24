import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from managers.notification_manager import NotificationManager
from managers.storage_manager import StorageManager

class NotificationFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.notification_manager = NotificationManager(StorageManager())
        self.user_id = None
        self.setup_ui()
        self.bind("<<ShowFrame>>", self.on_show_frame)
    
    def on_show_frame(self, event):
        """Mettre à jour les notifications lorsque le frame est affiché."""
        new_user_id = self.controller.user.get('user_id') if self.controller.user else None
        if self.user_id != new_user_id:
            self.user_id = new_user_id
        
        self.load_notifications()

    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Header
        header_frame = ttk.Frame(self)
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        ttk.Label(header_frame, text="Notifications", font=('Helvetica', 18, 'bold')).pack(side='left')
        
        # Bouton pour marquer toutes comme lues
        mark_all_read_btn = ttk.Button(header_frame, text="Marquer tout comme lu", 
                                      command=self.mark_all_as_read)
        mark_all_read_btn.pack(side='right')
        
        # Filtres
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filtrer par:").pack(side='left')
        
        self.filter_var = tk.StringVar(value="Toutes")
        filter_cb = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                 values=["Toutes", "Non lues", "Confirmations", "Annulations", "Changement", "Système"], 
                                 width=15, state="readonly")
        filter_cb.pack(side='left', padx=(10, 0))
        filter_cb.bind("<<ComboboxSelected>>", lambda e: self.load_notifications())
        
        refresh_btn = ttk.Button(filter_frame, text="Actualiser", command=self.load_notifications)
        refresh_btn.pack(side='right')
        
        # Liste des notifications
        list_frame = ttk.Frame(self)
        list_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Treeview pour les notifications
        columns = ("Date", "Type", "Message", "Statut")
        self.notifications_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        self.notifications_tree.heading('Date', text='Date')
        self.notifications_tree.column('Date', width=120, anchor='w')
        self.notifications_tree.heading('Type', text='Type')
        self.notifications_tree.column('Type', width=100, anchor='w')
        self.notifications_tree.heading('Message', text='Message')
        self.notifications_tree.column('Message', width=400, anchor='w')
        self.notifications_tree.heading('Statut', text='Statut')
        self.notifications_tree.column('Statut', width=80, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.notifications_tree.yview)
        self.notifications_tree.configure(yscrollcommand=scrollbar.set)
        
        self.notifications_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Actions
        actions_frame = ttk.Frame(self)
        actions_frame.pack(fill='x', padx=20, pady=(0, 20))
        
        ttk.Button(actions_frame, text="Marquer comme lu", command=self.mark_selected_as_read).pack(side='left', padx=(0, 10))
        ttk.Button(actions_frame, text="Supprimer", command=self.delete_selected).pack(side='left', padx=(0, 10))
        ttk.Button(actions_frame, text="Voir détails", command=self.view_details).pack(side='left')
    
    def load_notifications(self):
        """Charge les notifications dans la liste"""
        for item in self.notifications_tree.get_children():
            self.notifications_tree.delete(item)
        
        if not self.user_id:
            return

        # Récupérer les notifications selon le filtre
        filter_value = self.filter_var.get()
        
        notifications = self.notification_manager.get_notifications_for_user(self.user_id)

        if filter_value == "Non lues":
            notifications = [n for n in notifications if n.status == "unread"]
        elif filter_value == "Confirmations":
            notifications = [n for n in notifications if "confirm" in n.notification_type]
        elif filter_value == "Annulations":
            notifications = [n for n in notifications if "cancel" in n.notification_type]
        elif filter_value == "Changement":
            notifications = [n for n in notifications if "change" in n.notification_type]
        elif filter_value == "Système":
            notifications = [n for n in notifications if n.notification_type == "system"]
        
        # Trier par date (plus récent en premier)
        notifications.sort(key=lambda n: n.created_at, reverse=True)

        # Ajouter les notifications à la liste
        for notif in notifications:
            date_str = notif.created_at.strftime('%d/%m/%Y %H:%M')
            
            tags = ()
            if notif.status == "unread":
                tags = ("unread",)
            
            type_map = {
                "appointment_confirmation": "Confirmation",
                "appointment_cancellation": "Annulation",
                "appointment_validation": "Validation",
                "appointment_deletion": "Suppression",
                "status_change": "Changement",
                "system": "Système"
            }
            type_str = type_map.get(notif.notification_type, notif.notification_type.replace('_', ' ').title())
            
            self.notifications_tree.insert("", "end", values=(
                date_str,
                type_str,
                notif.message,
                "Non lu" if notif.status == "unread" else "Lu"
            ), tags=tags, iid=notif.notification_id)
        
        self.notifications_tree.tag_configure("unread", font=('Helvetica', 9, 'bold'))
    
    def mark_selected_as_read(self):
        """Marque la notification sélectionnée comme lue"""
        selected = self.notifications_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une notification")
            return
        
        notification_id = selected[0]
        if self.notification_manager.mark_notification_as_read(notification_id):
            self.load_notifications()
        else:
            messagebox.showerror("Erreur", "Impossible de marquer la notification comme lue")
    
    def mark_all_as_read(self):
        """Marque toutes les notifications comme lues"""
        if not self.user_id:
            return
        notifications = self.notification_manager.get_notifications_for_user(self.user_id, status="unread")
        count = 0
        
        for notif in notifications:
            if self.notification_manager.mark_notification_as_read(notif.notification_id):
                count += 1
        
        self.load_notifications()
        messagebox.showinfo("Succès", f"{count} notification(s) marquée(s) comme lue(s)")
    
    def delete_selected(self):
        """Supprime la notification sélectionnée"""
        selected = self.notifications_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une notification")
            return
        
        notification_id = selected[0]
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cette notification ?"):
            if self.notification_manager.delete_notification(notification_id):
                self.load_notifications()
                messagebox.showinfo("Succès", "Notification supprimée")
            else:
                messagebox.showerror("Erreur", "Impossible de supprimer la notification")
    
    def view_details(self):
        """Affiche les détails de la notification sélectionnée"""
        selected = self.notifications_tree.selection()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une notification")
            return
        
        notification_id = selected[0]
        
        if not self.user_id:
            return

        # Trouver la notification
        notifications = self.notification_manager.get_notifications_for_user(self.user_id)
        notification = None
        for notif in notifications:
            if notif.notification_id == notification_id:
                notification = notif
                break
        
        if notification:
            # Marquer comme lue en l'ouvrant
            if notification.status == 'unread':
                self.notification_manager.mark_notification_as_read(notification.notification_id)
                self.load_notifications() # Rafraîchir la liste

            # Créer une fenêtre de détails
            details_window = tk.Toplevel(self)
            details_window.title("Détails de la notification")
            details_window.geometry("500x400")
            details_window.resizable(False, False)
            
            # Centrer la fenêtre
            details_window.transient(self.controller)
            details_window.grab_set()
            
            # Contenu
            content_frame = ttk.Frame(details_window, padding=20)
            content_frame.pack(fill='both', expand=True)
            
            # Titre
            title_label = ttk.Label(content_frame, text=notification.message, font=('Helvetica', 14, 'bold'), wraplength=460, justify='left')
            title_label.pack(anchor='w', pady=(0, 10))
            
            # Date
            date_str = notification.created_at.strftime('%d/%m/%Y à %H:%M')
            
            ttk.Label(content_frame, text=f"Date: {date_str}", font=('Helvetica', 10)).pack(anchor='w', pady=(0, 5))
            
            # Type
            type_map = {
                "appointment_confirmation": "Confirmation de rendez-vous",
                "appointment_cancellation": "Annulation de rendez-vous",
                "appointment_validation": "Validation de rendez-vous",
                "appointment_deletion": "Suppression de rendez-vous",
                "status_change": "Changement de statut",
                "system": "Notification système"
            }
            type_str = type_map.get(notification.notification_type, "N/A")
            ttk.Label(content_frame, text=f"Type: {type_str}", font=('Helvetica', 10)).pack(anchor='w', pady=(0, 20))
            
            # Bouton OK
            ok_button = ttk.Button(content_frame, text="OK", command=details_window.destroy)
            ok_button.pack(side='bottom', pady=(10, 0)) 