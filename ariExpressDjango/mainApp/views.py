from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth import login as loginFunc
from django.contrib.auth import logout as logoutFunc, authenticate
from django.contrib.auth.forms import UserCreationForm
import os
import sys
from ProjectCode.Service.Service import Service
from .models import *
from .forms import *
from ProjectCode.Service.Response import *
from django.contrib.auth.models import User
from django.contrib import messages
import json
import ast
from django.contrib.auth.decorators import login_required 
from django.http import HttpResponseRedirect # for redirecting to another page and clearing the input fields
from django.contrib import messages # for displaying messages
from django.core.paginator import Paginator # for pagination
from datetime import datetime #used to get total msg per day
from django.views.decorators.cache import cache_control # for disabling cache



def startpage(request):
    return render(request, "startpage.html")

def mainpage(request):
    return render(request, 'mainpage.html')

def login(request):
    # service.logIn()
    msg = ""
    showMsg = False
    if request.method == 'POST':
        if request.user.is_authenticated:
            msg="A User is already logged in"
            form = None
        else:
            service = Service()
            form = loginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                res = service.logIn(username, password)
                msg = res.getStatus()
                if res.getStatus() == True:
                    user = authenticate(request, username=username, password=password)
                    msg="Logged in successfully"
                    loginFunc(request, user)
                    return redirect('mainApp:mainpage')
    else:
        form = loginForm()
        msg = ""
        showMsg = True


    return render(request, 'login.html', {'form': form,
                                          'msg': msg,
                                          'showMsg': showMsg})



def registerPage(request):
    msg = ""
    showMsg = False
    if request.method == 'POST':
        service = Service()
        if request.user.is_authenticated:
            msg="A User is already logged in"
            form = None
        else:
            form = CreateMemberForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                res = service.register(username, password, email)
                msg = res.getReturnValue()
                if res.getStatus() == True:
                    form.save()
                    user = authenticate(request, username=username, password=password)
                    loginFunc(request, user)
                    return redirect('mainApp:mainpage')


    else:
        form = CreateMemberForm()
        msg = ""
        showMsg = True


    return render(request, 'register.html', {'form': form,
                                          'msg': msg,
                                          'showMsg': showMsg})


def logout(request):
    msg = ""
    showMsg = False
    # if not request.user.is_authenticated:
    #     msg="User isn't logged in"
    #     form = None
    # service = Service()
    # res = service.logOut(username=request.user.username)
    # msg = res.getReturnValue()
    # if res.getStatus() == True:
    logoutFunc(request)
    return redirect('mainApp:mainpage')


    

def mystores(request):
    service = Service()
    # if request.method == 'POST' and request.user.is_authenticated:
    #     staffResposne = service.getStaffInfo(request.user.username, request.POST.get('storename'))
    #     if staffResposne.getStatus():
    #         staff = ast.literal_eval(str(staffResposne.getReturnValue()))
    #         return render(request, 'mystores.html', {'stores': storesInfoDict})

    
    storesInfo = service.getUserStores(request.user.username)
    string_data = storesInfo.getReturnValue()
    storesInfoDict = ast.literal_eval(str(string_data))
    # print(storesInfoDict)
    return render(request, 'mystores.html', {'stores': storesInfoDict})


def viewAllStores(request):
    service = Service()
    storesInfo = service.getStoresBasicInfo() 
    string_data = storesInfo.getReturnValue()
    storesInfoDict = ast.literal_eval(str(string_data))
    return render(request, 'allStores.html', {'stores': storesInfoDict})


def mystores_specific(request, storename):
    if request.method == 'POST' and request.user.is_authenticated:
        service = Service()
        products = service.getStoreProductsInfo(storename).getReturnValue()
        # context = request.POST.get('data')
        context = ast.literal_eval(str(products))
        products_dict = json.loads(context['products'])  # Parse JSON string into a dictionary
        active = "Open" if context['active'].lower() == "true" else "Closed"
        return render(request, 'shop_specific.html', {'products': products_dict,
                                                  'storename': storename,
                                                  'active': active})
    else:
        return redirect('mainApp:mainpage')
    

def openStore(request, storename):
    if request.method == 'POST' and request.user.is_authenticated:
        service = Service()
        actionRes = service.openStore(request.user.username, storename)
        if actionRes.getStatus():
            messages.success(request, ("Store is now open."))
            return redirect('mainApp:mystores_specific', storename=storename)
        else: 
            messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
            return redirect('mainApp:mystores')
    return redirect('mainApp:mainpage')
        

def closeStore(request, storename):
    if request.method == 'POST' and request.user.is_authenticated:
        service = Service()
        actionRes = service.closeStore(request.user.username, storename)
        if actionRes.getStatus():
            messages.success(request, ("Store is now closed."))
            return redirect('mainApp:mystores_specific', storename=storename)
        else: 
            messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
            return redirect('mainApp:mystores')
    return redirect('mainApp:mainpage')


def createStore(request):
    if request.method == 'POST' and request.user.is_authenticated:
        newStoreName = request.POST.get('storeName')
        service = Service()
        res = service.createStore(request.user.username, newStoreName)
        if res.getStatus():
            messages.success(request, ("A new store has been created successfully"))
            return redirect('mainApp:mystores')
        else:
            msg = res.getReturnValue()
            messages.success(request, (f"Error: {msg}"))
            return redirect('mainApp:mainpage')
    else:
        return render(request, 'createStore.html', {})
    

def nominateUser(request, storename):
    if request.method == 'POST':
        requesterUsername = request.user.username
        toBeNominatedUsername = request.POST.get('inputNominatedUsername')
        selected = request.POST.get('nominateSelect')
        store_name = request.POST.get('storename')
        service = Service()
        if selected == '1':
            res = service.nominateStoreOwner(requesterUsername, toBeNominatedUsername, store_name)
            if res.getStatus():
                messages.success(request, ("A new user has been nominated to be Owner."))
                return redirect('mainApp:mystores')
            else:
                messages.success(request, ("Error nominating a user to be Owner"))
                return redirect('mainApp:mystores')
        elif selected == '2':
            res = service.nominateStoreManager(requesterUsername, toBeNominatedUsername, store_name)
            if res.getStatus():
                messages.success(request, ("A new user has been nominated to be Manager."))
                return redirect('mainApp:mystores')
            else:
                messages.success(request, ("Error nominating a user to be Manager"))
                return redirect('mainApp:mystores')

    # messages.success(request, ("Error nominating a user to be Owner"))
    return render(request, 'nominateUser.html', {'storename': storename})


def addNewProduct(request, storename):
    if request.method == 'POST':
        form = NewProductForm(request.POST)
        if form.is_valid():
            productname = form.cleaned_data['productName']
            category = form.cleaned_data['productCategory']
            price = form.cleaned_data['productPrice']
            quantity = form.cleaned_data['productQuantity']
            service = Service()
            actionRes = service.addNewProductToStore(request.user.username, storename, productname, category, quantity, price)
            if actionRes.getStatus():
                print(actionRes.getReturnValue())
                messages.success(request, ("A new Product has been added to the store"))
                return redirect('mainApp:mystores')
            else:
                messages.success(request, (f"Error: {actionRes.getReturnValue()}"))
                return redirect('mainApp:mystores')
        else:
            # Handle the case when the form is invalid
            messages.error(request, "Invalid form data")
            return redirect('mainApp:addNewProduct', storename=storename)
    else:
        form = NewProductForm()

    return render(request, 'addNewProduct.html', {'storename': storename})


def adminPage(request):
    if request.user.is_superuser:
        return render(request, 'adminPage.html', {})
    else:
        messages.success(request, ("Cannot access ADMIN area because you are not an admin."))
        return redirect('mainApp:mainpage')

def viewOnlineUsers(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            service = Service()
            resOnline = service.getAllOnlineMembers(request.user.username)
            resOffline = service.getAllOfflineMembers(request.user.username)
            if resOnline.getStatus() and resOffline.getStatus():
                onlinemembers = resOnline.getReturnValue() #returns a list
                offlinemembers = resOffline.getReturnValue() #returns a list
                onlinemembers = ast.literal_eval(str(onlinemembers))
                offlinemembers = ast.literal_eval(str(offlinemembers))
                context = {'online': onlinemembers,
                        'offline': offlinemembers}
                return render(request, 'adminPage.html', {'context': context})
        
    messages.success(request, ("Cannot access ADMIN area because you are not an admin."))
    return redirect('mainApp:mainpage')

def reset_password(request):
    pass

def homepage_guest(request):
    pass



@login_required(login_url='/login')
def inbox(request):
    all_user_messages = UserMessage.objects.filter(receiver=request.user.username).order_by('-creation_date')
    pending = UserMessage.objects.filter(receiver=request.user.username, status='pending').count()
    paginator = Paginator(all_user_messages, 3)
    page = request.GET.get('page')
    all_messages = paginator.get_page(page)
    return render(request, 'inbox.html',{'usermessages': all_messages, 'pending': pending})


def send_message(request):
    if request.method == 'POST':
        service = Service()
        form = UserMessageform(request.POST, request.FILES)
        if form.is_valid():
            receiver_username = form.cleaned_data['receiver']
            res = service.checkUsernameExistence(receiver_username)
            if res.getStatus():
                message = form.save(commit=False)
                message.sender = request.user.username
                message.save()
                messages.success(request, "Message sent successfully")
                return HttpResponseRedirect('/inbox')
            else:
                messages.error(request, "Invalid adresssee username - the message was not sent")
        else:
            messages.error(request, "Invalid form submission")
    else:
        form = UserMessageform()
        messages.error(request, "Error sending message")
    return HttpResponseRedirect('/inbox')   


@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_message(request, usermessage_id):
    message = UserMessage.objects.get(id=usermessage_id)
    message.delete()
    messages.success(request, "Message deleted successfully")
    return HttpResponseRedirect('/inbox')



@login_required(login_url='/login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mark_as_read(request, usermessage_id):
    message = UserMessage.objects.get(id=usermessage_id)
    message.status = 'read'
    message.save()
    messages.success(request, "Message marked as read successfully")
    return HttpResponseRedirect('/inbox')


# check if username exists
def check_username(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        service = Service()
        res = service.checkUsernameExistence(username)
        if res.getStatus():
            return JsonResponse({'status': True})
        else:
            return JsonResponse({'status': False}) 

@login_required(login_url='/login')
def notifications(request):
    pending = UserMessage.objects.filter(receiver=request.user.username, status='pending').count()



#cart functionality
def cart(request):
    if request.user.is_authenticated:
        service = Service()
        res = service.getCart(request.user.username)
        if res.getStatus():
            cart = res.getReturnValue()
            baskets = ast.literal_eval(str(cart)).get('baskets')
            baskets = ast.literal_eval(str(baskets))
            products = dict()
            for basket in baskets:
                basket_res = service.getBasket(request.user.username, basket['storename'])
                if basket_res.getStatus()==True:
                    basket_res = basket_res.getReturnValue()
                    basket_products = ast.literal_eval(str(basket_res)).get('products')
                    basket_products = ast.literal_eval(str(basket_products))
                    products[basket['storename']] = basket_products

            return render(request, 'cart.html', {'baskets': baskets , 'products': products})
        else:
            messages.error(request, "Error loading cart - "+str(res.getReturnValue()))
            return redirect('mainApp:mainpage')
    else:
        messages.error(request, "You must be logged in to view your cart")
        return HttpResponseRedirect('/login')
    