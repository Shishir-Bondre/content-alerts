def email_subject(center_name):
    return f"[Urgent Reminder] Vaccine slot is now available at {center_name}"


def email_body(email_data):
    return f"Hi, \n" \
           f"Vaccine slot is available for below centers \n " \
           f"Center name and available data \n  {email_data} \n" \
           f"Please register at cowin website https://cowin.gov.in \n" \
           f"Have a lovely day ahead! :) \n" \
           f"Thanks, \n" \
           f"Shishir Bondre \n" \
           f"To unsubscribe click here http://3.6.160.147:8000/vaccine_tracker/unsubscribe/"

