import requests
import logging
import pytz

from django.core.mail import EmailMessage
from vaccine_tracker.models import UsersData
from celery import shared_task
from tracker.celery import app
from vaccine_tracker.email import email_body, email_subject
from django.conf import settings
from django_celery_results.models import TaskResult
from datetime import datetime, timedelta



logger = logging.getLogger(__name__)

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

@app.task
def clean_up_task_result_every_15_mins():
    time_threshold = datetime.now(tz=pytz.UTC) - timedelta(minutes=10)
    tasks = TaskResult.objects.filter(date_created__lt=time_threshold)
    try:
        tasks.delete()
    except Exception as e:
        logger.info("[INFO] Cannot delete")
    else:
        logger.info("[INFO] Deleted tasks results")

@app.task
def check_for_slot_every_15_mins():
    users = UsersData.objects.all()
    for user in users:
        print(user.district_id, user.pincode, user.district_name, user.email_id, user.min_age_limit)
        email_data = check_slot_available(user.district_id, user.district_name, user.pincode, user.min_age_limit)
        if len(email_data) > 0:
            SendEmailTask.delay(user.district_name, to_email=[user.email_id], email_data=email_data)

@shared_task
def SendEmailTask(district_name, to_email, email_data):
    """
    Celery task for sending email. uses default django mailer
    Please do configure email settings in settings.py file
    :param email_data:
    :param to_email: to email
    :return:
    """

    email = EmailMessage(subject=email_subject(district_name),
                         body=email_body(email_data),
                         from_email=settings.EMAIL_HOST_USER,
                         to=to_email)

    logger.info(f'[INFO] Sending email to {to_email}')
    email.send()
    logger.info(f'[INFO] Email has been successfully send')


def check_slot_available(district_id, district_name, pincode, age_limit=18):
    date = datetime.now().strftime("%d-%m-%Y")
    response = requests.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public"
                            f"/calendarByDistrict?district_id={district_id}&date={date}", headers=headers)

    email_data = []
    if response.status_code == 200:
        print("got the response now checking")
        json = response.json()
        centers = json.get('centers')
        for center in centers:
            if center.get('pincode') == pincode or center.get('district_name') == district_name:
                for session in center.get('sessions'):
                    capacity = []
                    if session.get('available_capacity') >= 2:
                        if session.get('min_age_limit') == int(age_limit):
                            capacity.append({'available_capacity': session.get('available_capacity'), 'date': session.get('date')})
                if len(capacity) >= 1:
                    email_data.append({'center_name': center.get('name'), 'pincode': center.get('pincode'), 'available_capacity': capacity})
    return email_data
