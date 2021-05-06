from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('vaccine_tracker/', include('vaccine_tracker.urls')),
    path('admin/', admin.site.urls),
]
