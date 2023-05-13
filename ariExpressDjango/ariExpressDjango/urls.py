from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('mainApp.urls')),
    
]
