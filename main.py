# Point d'entrée principal de l'application (version GUI uniquement)
import tkinter as tk
from gui.main_app import MainApplication

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApplication(root)
    root.mainloop() 