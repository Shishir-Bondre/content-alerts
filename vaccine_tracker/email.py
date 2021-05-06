def email_subject(center_name):
    return f"[Urgent Reminder] Vaccine slot is now available at {center_name}"


def email_body(center_name, pincode, date, capacity):
    return f"Hi, \n" \
           f"Vaccine slot is available at  {center_name} , {pincode} " \
           f"for date {date}  \n" \
           f" vaccine availability is {capacity} " \
           f"Please register at cowin website https://cowin.gov.in \n" \
           f"Have a lovely day ahead! :) \n" \
           f"Thanks, \n"

