from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path(r'', views.homepage, name="homepage"),
    path(r'login', views.login, name='login'),
    path(r'about/', views.about),
    path(r'member/', views.member, name='member'),
    path(r'member/found', views.memberfound, name='memberfound'),
    # path(r'register', views.register, name='register_form'),
    # path(r'resetpassword', views.reset_password, name='reset_password'),
    
    
]