from django.core.mail import send_mail
from django.conf import settings
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_timetable.settings')
django.setup()

def test_email():
    try:
        send_mail(
            'Test Email from Django',
            'This is a test email to verify the email configuration.',
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        print("Test email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

if __name__ == "__main__":
    test_email() 