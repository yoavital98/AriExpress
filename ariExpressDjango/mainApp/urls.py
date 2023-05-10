from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "mainApp"

urlpatterns = [
    path(r'', views.startpage, name="startpage"),
    path(r'login/', views.login, name="login"),
    path(r'logout/', views.logout, name="logout"),
    path(r'home/', views.mainpage, name="mainpage"),
    path(r'register/', views.registerPage, name='registerPage'),
    
    
]