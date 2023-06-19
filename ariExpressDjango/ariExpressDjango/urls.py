from django.contrib import admin
from django.urls import path, include
import notifications.urls

from ProjectCode.Domain.ExternalServices.MessageObjects import routing

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('', include('mainApp.urls')),
    path ('inbox/notifications/' , include(notifications.urls, namespace = 'notifications' )),
    
]
websocket_urlpatterns = routing.websocket_urlpatterns
