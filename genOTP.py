import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(email, otp):
    # Replace these values with your Gmail account details
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'usermail'
    smtp_password = 'password'

    sender_email = 'senderemail'
    receiver_email = email

    subject = 'Your OTP'
    body = f'Your OTP is: {otp}'

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"OTP sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending OTP: {e}")

# Example usage in genOTP.py
if __name__ == "__main__":
    email = input("Enter your Gmail email: ")
    otp = generate_otp()
    send_otp(email, otp)
