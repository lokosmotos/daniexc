import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from twilio.rest import Client

# Email Configuration
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Twilio Configuration
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_NUMBER = os.getenv('TWILIO_NUMBER')

def render_template(template_name, context):
    with open(f'templates/{template_name}') as file:
        return Template(file.read()).render(**context)

def send_email(to, subject, template_name, context):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = to
        msg['Subject'] = subject
        
        html = render_template(template_name, context)
        msg.attach(MIMEText(html, 'html'))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_sms(to, message):
    try:
        client = Client(TWILIO_SID, TWILIO_TOKEN)
        message = client.messages.create(
            body=message,
            from_=TWILIO_NUMBER,
            to=to
        )
        return True
    except Exception as e:
        print(f"SMS error: {e}")
        return False

# Message Templates
def send_interview_reminder(candidate):
    context = {
        'name': candidate['name'],
        'position': candidate['position'],
        'time': candidate['interview_time'],
        'branch': candidate['branch'],
        'template_type': 'interview'
    }
    return send_email(
        candidate['email'],
        "🐾 Interview Reminder - Cat Grooming Inc",
        "email_template.html",
        context
    )

def send_no_show_alert(candidate):
    context = {
        'name': candidate['name'],
        'position': candidate['position'],
        'template_type': 'no_show'
    }
    sms_message = (
        f"Hi {candidate['name']}, we missed you on your first day! "
        f"Please contact us to reschedule your {candidate['position']} position."
    )
    
    email_sent = send_email(
        candidate['email'],
        "😿 We Missed You - Cat Grooming Inc",
        "email_template.html",
        context
    )
    sms_sent = send_sms(candidate['phone'], sms_message)
    
    return email_sent and sms_sent

def send_standby_inquiry(candidate):
    sms_message = (
        f"Hi {candidate['name']}, are you available for "
        f"part-time {candidate['position']} work this week? Reply YES/NO"
    )
    return send_sms(candidate['phone'], sms_message)
