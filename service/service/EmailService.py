from django.core.mail import send_mail

class EmailService:

    @staticmethod
    def send(msg):
        send_mail(msg.subject, msg.text, msg.frm, msg.to, fail_silently=False, html_message=msg.text)
