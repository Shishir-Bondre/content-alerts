from django.db import models


class UsersData(models.Model):
    email_id = models.EmailField()
    pincode = models.CharField(max_length=6)
    mobile_no = models.CharField(max_length=12)
    min_age_limit = models.CharField(max_length=100)
    district_id = models.CharField(max_length=100)
    district_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
