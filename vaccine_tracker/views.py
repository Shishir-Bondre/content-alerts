import requests
import json
from django.http import HttpResponse
from django.shortcuts import render
from vaccine_tracker.models import UsersData


def get_district(request):
    state_id = request.POST['state_id']
    response = requests.get(f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{state_id}")
    if response.status_code == 200:
        json = response.json()
        return render(request, "vaccine_tracker/index.html",
                      context={'districts': json.get('districts')})
    return HttpResponse("Not available")


def index(request):
    response = requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states")
    print(response.status_code)
    print("inside index")
    if response.status_code == 200:
        print(response.json())
        json = response.json()
        return render(request, "vaccine_tracker/index.html", context={'states': json.get('states')})
    return HttpResponse("Not available")


def start_tracker(request):
    pincode = request.POST['pincode']
    email_id = request.POST['email_id']
    mobile_no = request.POST['mobile_no']
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
