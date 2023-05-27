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
    path(r'mystores/', views.mystores, name="mystores"),
    path(r'allstores/', views.viewAllStores, name="viewAllStores"),
    path(r'inbox/', views.inbox, name='inbox'),
    # path(r'resetpassword', views.reset_password, name='reset_password'),
    path(r'mystores/<str:storename>/', views.mystores_specific, name='mystores_specific'),
    path(r'createStore/', views.createStore, name='createStore'),
    path(r'nominate/<str:storename>/', views.nominateUser, name='nominateUser'),
    path(r'adminPage/', views.adminPage, name='adminPage'),
    path(r'adminPage/OnlineUsers', views.viewOnlineUsers, name='viewOnlineUsers'),
    # path to send the message
    path(r'send_message', views.send_message, name='send_message'),
    path(r'check_username/', views.check_username, name='check_username'),
    # path to delete the message
    path(r'delete_message/<str:usermessage_id>', views.delete_message, name='delete_message'),
    # path to view the message
    path (r'mark_as_read/<str:usermessage_id>', views.mark_as_read, name='mark_as_read'),
    path(r'cart/', views.cart, name='cart'),
    path(r'remove_product', views.remove_product, name='remove_product'),
    path(r'edit_product', views.edit_product, name='edit_product'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)