from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail

@shared_task()
def send_notification_email(subject: str, message: str, recipient_email: str) -> None:
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [recipient_email],
        fail_silently=False,
    )