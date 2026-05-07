import logging
import threading

from django.core.mail import send_mail

logger = logging.getLogger(__name__)


class EmailService:

    @staticmethod
    def send(msg):
        def _send():
            try:
                send_mail(
                    msg.subject,
                    msg.text,
                    msg.frm,
                    msg.to,
                    fail_silently=False,
                    html_message=msg.text,
                )
            except Exception as e:
                logger.exception("Failed to send email to %s: %s", msg.to, e)

        threading.Thread(target=_send, daemon=True).start()
