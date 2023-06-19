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
    path(r'store/<str:storename>/', views.store_specific, name='store_specific'),
    path(r'createStore/', views.createStore, name='createStore'),
    # path(r'openStore/<str:storename>', views.openStore, name='openStore'),
    # path(r'closeStore/<str:storename>', views.closeStore, name='closeStore'),
    path(r'addNewProduct/<str:storename>', views.addNewProduct, name='addNewProduct'),
    path(r'editProduct/<str:storename>', views.editProduct, name='editProduct'),
    path(r'addNewDiscount/<str:storename>', views.addNewDiscount, name='addNewDiscount'),
    path(r'addNewDiscountSpecial/<str:storename>/<str:discount_type>', views.addNewDiscountSpecial, name='addNewDiscountSpecial'),
    
    path(r'addNewPurchasePolicy/<str:storename>', views.addNewPurchasePolicy, name='addNewPurchasePolicy'),
    path(r'viewDiscounts/<str:storename>', views.viewDiscounts, name='viewDiscounts'),
    path(r'viewBids/<str:storename>', views.viewBids, name='viewBids'),
    path(r'userBids/', views.userBids, name='userBids'),
    path(r'viewStoreStaff/<str:storename>', views.viewStoreStaff, name='viewStoreStaff'),

    path(r'nominate/<str:storename>/', views.nominateUser, name='nominateUser'),
    path(r'adminPage/', views.adminPage, name='adminPage'),
    path(r'adminPage/OnlineUsers', views.viewOnlineUsers, name='viewOnlineUsers'),
    # path to send the message
    path(r'send_message', views.send_message, name='send_message'),
    path(r'check_username/', views.check_username, name='check_username'),
    # path to delete the message
    path(r'delete_message/<str:usermessage_id>', views.delete_message, name='delete_message'),
    path(r'delete_notification/<str:notification_id>', views.delete_notification, name='delete_notification'),
    # path to view the message
    path (r'inbox/mark_as_read/<str:usermessage_id>', views.mark_as_read, name='mark_as_read'),
    path (r'inbox/mark_notification_as_read/<str:notification_id>', views.mark_notification_as_read, name='mark_notification_as_read'),
    path(r'cart/', views.cart, name='cart'),
    path(r'remove_basket_product', views.remove_basket_product, name='remove_basket_product'),
    path(r'edit_basket_product', views.edit_basket_product, name='edit_basket_product'),
    path(r'add_product_to_cart',views.add_product_to_cart, name='add_product_to_cart'),
    path(r'checkoutpage/', views.checkoutpage, name='checkoutpage'),
    path(r'bidcheckoutpage/', views.checkoutpage_bids, name='bidcheckoutpage'),
    path(r'checkout', views.checkout, name='checkout'),
    path(r'checkout_bid', views.checkout_bid, name='checkout_bid'),
    path(r'searchpage/', views.searchpage, name='searchpage'),
    path(r'userPurchaseHistory/', views.userPurchaseHistory, name='userPurchaseHistory'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)