import smtplib
from email.message import EmailMessage

from config import (
    EMAIL_ENABLED, SENDER_EMAIL, SENDER_PASSWORD,
    AUTHORITY_EMAIL, SMTP_SERVER, SMTP_PORT,
)
from utils.logger import get_logger

logger = get_logger(__name__)


def send_report_email(predicted_class, confidence, lat, lon, maps_link,
                       image_bytes, image_filename="report.jpg"):
    
    if not EMAIL_ENABLED:
        return False, "Email sending is disabled. Set EMAIL_ENABLED = True in config.py once credentials are filled in."

    try:
        msg = EmailMessage()
        msg["Subject"] = f"Road Damage Report: {predicted_class}"
        msg["From"] = SENDER_EMAIL
        msg["To"] = AUTHORITY_EMAIL
        msg.set_content(
            f"""A road issue has been reported.

Predicted class: {predicted_class}
Confidence: {confidence * 100:.2f}%
Location: {lat}, {lon}
Google Maps link: {maps_link}

(Image attached)
"""
        )
        msg.add_attachment(image_bytes, maintype="image", subtype="jpeg", filename=image_filename)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        logger.info(f"Report email sent for {predicted_class} at {lat},{lon}")
        return True, "Report emailed successfully."

    except Exception as e:
        logger.error(f"Failed to send report email: {e}")
        return False, f"Failed to send email: {e}"