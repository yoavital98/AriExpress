from django.contrib import admin
from django.urls import path, include

from ProjectCode.Domain.ExternalServices.MessageObjects import routing
from . import views

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('mainApp.urls')),
    
]
websocket_urlpatterns = routing.websocket_urlpatterns
