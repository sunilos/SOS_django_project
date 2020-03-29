from django.core.mail import send_mail
from SOS_django_projects.settings import EMAIL_HOST_USER, BASE_DIR
from string import Template
from .EmailBuilder import EmailBuilder

class EmailService:

    @staticmethod
    def send(msg):
        send_mail(msg.subject, msg.text, msg.frm, msg.to, fail_silently = False)
