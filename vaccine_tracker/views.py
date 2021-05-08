import requests
import json
from django.http import HttpResponse
from django.shortcuts import render
from vaccine_tracker.models import UsersData
from vaccine_tracker.tasks import SendEmailTask


headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

def get_district(request):
    state_id = request.POST['state_id']
    response = requests.get(f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}", headers=headers)
    if response.status_code == 200:
        json = response.json()
        return render(request, "vaccine_tracker/index.html",
                      context={'districts': json.get('districts')})
    return HttpResponse("Not available")


def send_dummy_email(request):
    if request.method == "GET":
        return render(request, "vaccine_tracker/trail.html")
    email_id = request.POST['email_id']
    SendEmailTask.delay("dummy", to_email=[email_id], email_data=[{"center_name": "Dummy"}])
    return HttpResponse("Email sent, Please check your spam folder and mark it as not spam")


def index(request):
    response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states", headers=headers)
    if response.status_code == 200:
        print("Got the states",response.status_code)
        json = response.json()
        return render(request, "vaccine_tracker/index.html", context={'states': json.get('states')})
    return HttpResponse(f"Not available bcoz {response.status_code}")

def unsubscribe(request):
    if request.method == "GET":
        return render(request, "vaccine_tracker/unsubscribe.html")

    email_id = request.POST['email_id']
    try:
        users = UsersData.objects.get(email_id=email_id)
    except (KeyError, UsersData.DoesNotExist):
        return HttpResponse("User not found. Go back")
    else:
        users.delete()
    return HttpResponse("unsubscribe successfully")

def start_tracker(request):
    pincode = request.POST['pincode']
    email_id = request.POST['email_id']
    mobile_no = "9876543210"
    min_age_limit = request.POST['min_age_limit']
    district = request.POST['district']
    district = json.loads(district.replace("\'", "\""))
    district_name = district.get('district_name')
    district_id = district.get('district_id')
    try:
        users = UsersData.objects.get(email_id=email_id)
    except (KeyError, UsersData.DoesNotExist):
        UsersData.objects.create(pincode=pincode, email_id=email_id,
                                 mobile_no=mobile_no, min_age_limit=min_age_limit,
                                 district_id=district_id, district_name=district_name)
    else:
        users.pincode = pincode
        users.mobile_no = mobile_no
        users.min_age_limit = min_age_limit
        users.district_id = district_id
        users.district_name = district_name
        users.save()

    return render(request, "vaccine_tracker/back.html")
