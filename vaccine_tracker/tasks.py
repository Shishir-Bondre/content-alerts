import requests
import datetime
import logging

from django.core.mail import EmailMessage
from vaccine_tracker.models import UsersData
from celery import shared_task
from tracker.celery import app
from vaccine_tracker.email import email_body, email_subject
from django.conf import settings

logger = logging.getLogger(__name__)


@app.task
def check_for_slot_every_15_mins():
    users = UsersData.objects.all()
    for user in users:
        print(user.district_id, user.pincode, user.district_name, user.email_id, user.min_age_limit)
        check_slot_available(user.district_id, user.district_name, user.pincode, user.email_id, user.min_age_limit)


@shared_task
def SendEmailTask(to_email, center_name, pincode, date, capacity):
    """
    Celery task for sending email. uses default django mailer
    Please do configure email settings in settings.py file
    :param center_name:
    :param pincode:
    :param date:
    :param capacity:
    :param to_email: to email
    :return:
    """

    email = EmailMessage(subject=email_subject(center_name),
                         body=email_body(center_name, pincode, date, capacity),
                         from_email=settings.EMAIL_HOST_USER,
                         to=to_email)

    logger.info(f'[INFO] Sending email to {to_email}')
    email.send()
    logger.info(f'[INFO] Email has been successfully send')


def check_slot_available(district_id, district_name, pincode, email_id, age_limit=18):
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    response = requests.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public"
                            f"/calendarByDistrict?district_id={district_id}&date={date}")

    if response.status_code == 200:
        print("got the response now checking")
        json = response.json()
        centers = json.get('centers')
        for center in centers:
            if center.get('pincode') == pincode or center.get('district_name') == district_name:
                for session in center.get('sessions'):
                    if session.get('available_capacity') >= 0:
                        if session.get('min_age_limit') == int(age_limit):
                            SendEmailTask.delay(to_email=[email_id], center_name=center.get('name'),
                                                pincode=pincode, date=session.get('date'),
                                                capacity=session.get('available_capacity'))
