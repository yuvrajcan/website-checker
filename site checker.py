import requests
import smtplib
import schedule
import time

# Configuration
URL = 'http://example.com'
CHECK_INTERVAL = 5  # in minutes
EMAIL_ADDRESS = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_email_password'
NOTIFY_EMAIL = 'notify_email@gmail.com'

def check_website():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            print(f"{URL} is up.")
        else:
            print(f"{URL} is down. Status code: {response.status_code}")
            notify_user(f"{URL} is down. Status code: {response.status_code}")
    except requests.ConnectionError:
        print(f"{URL} is down. Failed to connect.")
        notify_user(f"{URL} is down. Failed to connect.")

def notify_user(message):
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            subject = 'Website Down Alert'
            body = f'Subject: {subject}\n\n{message}'
            server.sendmail(EMAIL_ADDRESS, NOTIFY_EMAIL, body)
            print("Notification email sent.")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

def main():
    schedule.every(CHECK_INTERVAL).minutes.do(check_website)
    
    print(f"Starting site checker for {URL} every {CHECK_INTERVAL} minutes.")
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
