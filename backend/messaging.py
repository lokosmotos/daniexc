import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template

def render_template(template_name, context):
    with open(f'templates/{template_name}') as file:
        return Template(file.read()).render(**context)

def send_email(to, subject, template, context):
    msg = MIMEMultipart()
    msg['From'] = 'hr@catgrooming.com'
    msg['To'] = to
    msg['Subject'] = subject
    
    html = render_template(template, context)
    msg.attach(MIMEText(html, 'html'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
        server.send_message(msg)

def send_interview_reminder(candidate):
    context = {
        'name': candidate['name'],
        'position': candidate['position'],
        'time': candidate['interview_time'],
        'branch': candidate['branch']
    }
    send_email(
        candidate['email'],
        "Interview Reminder - Cat Grooming Inc",
        "email_template.html",
        context
    )

def send_sms_via_twilio(number, message):
    # Implement Twilio integration here
    pass
