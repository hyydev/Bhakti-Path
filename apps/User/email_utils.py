# apps/User/email_utils.py

import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


def send_otp_email(user_email: str, user_name: str, otp_code: str) -> bool:
    """
    Registration OTP email bhejo.

    Returns:
        True  → email gayi
        False → email fail hui (log ho jaayega)
    """
    subject = "BhaktiPath — Verify Your Email"

    message = f"""
Namaste {user_name}!

Welcome to BhaktiPath — Your Devotional Shopping Destination.

Your OTP to verify your email address is:

    {otp_code}

This OTP is valid for 10 minutes only.
Do not share this OTP with anyone.

If you did not create an account, please ignore this email.

With Devotion,
Team BhaktiPath
    """.strip()

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=f"{settings.DEFAULT_FROM_NAME} <{settings.DEFAULT_FROM_EMAIL}>",
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info(f"OTP email sent to {user_email}")
        return True

    except Exception as e:
        logger.error(f"OTP email failed for {user_email}: {str(e)}")
        return False


def send_password_reset_email(user_email: str, user_name: str, otp_code: str) -> bool:
    """
    Password reset OTP email bhejo.
    """
    subject = "BhaktiPath — Password Reset OTP"

    message = f"""
Namaste {user_name}!

We received a request to reset your BhaktiPath password.

Your OTP to reset password is:

    {otp_code}

This OTP is valid for 10 minutes only.
Do not share this OTP with anyone.

If you did not request this, please ignore this email.

With Devotion,
Team BhaktiPath
    """.strip()

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=f"{settings.DEFAULT_FROM_NAME} <{settings.DEFAULT_FROM_EMAIL}>",
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info(f"Password reset email sent to {user_email}")
        return True

    except Exception as e:
        logger.error(f"Password reset email failed for {user_email}: {str(e)}")
        return False
