"""
Celery-backed transactional email senders: welcome, verification,
password reset, invoice, shipping updates.
"""
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_welcome_email(user_email: str, user_name: str):
    send_mail(
        subject="Welcome to WEBTECH",
        message=f"Hi {user_name}, welcome to WEBTECH — the future of technology.",
        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, "DEFAULT_FROM_EMAIL") else None,
        recipient_list=[user_email],
    )


# TODO: send_verification_email, send_password_reset_email, send_invoice_email, send_shipping_email
