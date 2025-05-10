import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
import json
from datetime import datetime, timedelta

# charge les rdv via ton fichier Erick
def load_appointments(filename="rendezvous.json"):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            appointments = json.load(file)
        return appointments
    except Exception as e:
        print("Erreur de lecture du fichier JSON :", e)
        return []

# Fonction pour envoyer un email
def send_email(subject, body, to_email):
    from_email = "testpython@gmail.com"  # faut mettre son mail ici ;)
    password = "tumetcequetuveux"  

    msg = MIMEMultipart()
    msg["From"] = from_email  
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print(f"Rappel envoyé à {to_email} : {subject}")
    except Exception as e:
        print("Erreur d'envoi :", e)

# ça vérifie le rdv de demain et ça envoie un rappel ici
def schedule_reminders():
    appointments = load_appointments()
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    for appointment in appointments:
        if appointment["date"] == tomorrow:
            schedule.every().day.at("08:00").do(
                send_email,
                subject=appointment["subject"],
                body=appointment["body"],
                to_email=appointment["to_email"]
            )
    print("Rappels programmés.")

# Boucle principale pour exécuter les tâches programmées
if __name__ == "__main__":
    schedule_reminders()
    while True:
        schedule.run_pending()
        time.sleep(60)
