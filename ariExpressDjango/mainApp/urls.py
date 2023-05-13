from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from ariExpressDjango import settings

app_name = "mainApp"

urlpatterns = [
    path(r'', views.mainpage, name="mainpage"),
    path(r'login/', views.login, name="login"),
    path(r'logout/', views.logout, name="logout"),
    # path(r'home/', views.mainpage, name="mainpage"),
    path(r'register/', views.registerPage, name='registerPage'),
    path(r'myshops/', views.myshops, name="myshops"),
    path(r'inbox/', views.inbox, name='inbox'),
    # path(r'resetpassword', views.reset_password, name='reset_password'),
    path (r'myshops/<str:shopname>/', views.myshops_specific, name='myshops_specific'),
    path (r'nominate/<str:shopname>/', views.nominateUser, name='nominateUser'),
    path (r'adminPage/', views.adminPage, name='adminPage'),
    path (r'adminPage/OnlineUsers', views.viewOnlineUsers, name='viewOnlineUsers'),
    # path to send the message
    path (r'send_message/<str:username>/', views.send_message, name='send_message'),

    
]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)