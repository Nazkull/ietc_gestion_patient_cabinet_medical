import tkinter as tk
from tkinter import ttk

class WelcomeFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), padding=10)
        style.configure('TLabel', font=('Helvetica', 18, 'bold'))

        label = ttk.Label(self, text="Welcome to the Medical Office")
        label.pack(pady=40)

        login_button = ttk.Button(self, text="Login", 
                                  command=lambda: print("Login button pressed"))
                                  # Later: command=lambda: controller.show_frame(LoginFrame))
        login_button.pack(pady=10)

        register_button = ttk.Button(self, text="Register", 
                                     command=lambda: print("Register button pressed"))
                                     # Later: command=lambda: controller.show_frame(RegisterFrame))
        register_button.pack(pady=10) 