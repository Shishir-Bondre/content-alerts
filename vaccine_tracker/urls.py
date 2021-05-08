from django.urls import path

from vaccine_tracker import views

urlpatterns = [
    path("", views.index, name="index"),
    path("trail/", views.send_dummy_email, name="trail"),
    path("startTracker/", views.start_tracker, name="tracker"),
    path("district/", views.get_district, name="district"),
    path("unsubscribe/", views.unsubscribe, name="unsubscribe")
]
