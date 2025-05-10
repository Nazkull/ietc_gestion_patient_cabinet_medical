import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time

# je fais une fonction pour envoyer un email
def send_email(subject, body, to_email):
    from_email = "Denitest@gmail.com" 
    password = "testpython" 

# détails du message

    msg = MIMEMultipart()
    msg["From"] = from_email  
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # connection au serveur gmail
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("Email reminder sent.")
    except Exception as e:
        print("Error sending email:", e)
    
    # rappel automatique qui est fixé à 8H du sbah

def schedule_reminder():
    schedule.every().day.at("08:00").do(
        send_email, 
        subject="Reminder: Event Tomorrow", 
        body="Don't forget—your event is coming up tomorrow!", 
        to_email="recipient_email@example.com"
    )
    # boucle pour surveille les taches programmées
if __name__ == "__main__":
    schedule_reminder()
    while True:
        schedule.run_pending()
        time.sleep(60)