# ~/automation/fullstack_ztp/fullstack_ztp/urls.py

from django.contrib import admin
from django.urls import path, include   # NEW

from .views import homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage, name='homepage'),
    path('ztp/', include('ztp.urls')),  # NEW
]