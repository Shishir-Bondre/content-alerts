from django.urls import path

from vaccine_tracker import views

urlpatterns = [
    path("", views.index, name="index"),
    path("startTracker/", views.start_tracker, name="tracker"),
    path("district/", views.get_district, name="district")
]
