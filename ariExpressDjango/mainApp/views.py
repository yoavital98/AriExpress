from django.http import HttpResponse
from django.shortcuts import render, redirect
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


    

def myshops(request):
    # service = Service()
    # stores = Store.objects.filter(store_name='')
    stores = {'store1': {'store_name': "Aqew Store",
                         'active': True,
                         'products': {'name': "Banana"}},
            'store2': {'store_name': "BulBul Store",
                        'active': False,
                        'products': {'name': "Apple"}}}
    # products = Product.objects.all()
    return render(request, 'myshops.html', {'stores': stores})


def myshops_specific(request, shopname):
    context = None
    if request.method == 'POST':
        context = request.POST.get('data')
        # print(context)
        context = ast.literal_eval(str(context))

    else:
        return redirect('mainApp:mainpage')
    return render(request, 'shop_specific.html', {'context': context,
                                                  'shopname': shopname})

def nominateUser(request, shopname):
    if request.method == 'POST':
        requesterUsername = request.user.username
        toBeNominatedUsername = request.POST.get('inputNominatedUsername')
        selected = request.POST.get('nominateSelect')
        store_name = request.POST.get('storename')
        service = Service()
        if selected == '1':
            res = service.nominateStoreOwner(requesterUsername, toBeNominatedUsername, store_name)
            # Mock part: assume it returns a dictionary
            # res = {'status': True,
            #            'object': "Something"
            #            }
            # if res.get('status'):
            if res.getStatus():
                messages.success(request, ("A new user has been nominated to be Owner."))
                return redirect('mainApp:myshops')
            else:
                messages.success(request, ("Error nominating a user to be Owner"))
                return redirect('mainApp:myshops')
        elif selected == '2':
            res = service.nominateStoreManager(requesterUsername, toBeNominatedUsername, store_name)
            # Mock part: assume it returns a dictionary
            res = {'status': True,
                       'object': "Something"
                       }
            if res.get('status'):
            # if res.getStatus():
                messages.success(request, ("A new user has been nominated to be Manager."))
                return redirect('mainApp:myshops')
            else:
                messages.success(request, ("Error nominating a user to be Manager"))
                return redirect('mainApp:myshops')

    # messages.success(request, ("Error nominating a user to be Owner"))
    return render(request, 'nominateUser.html', {'shopname': shopname})

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



@login_required(login_url='mainApp:login')
def inbox(request):
    return render(request, 'inbox.html')

@login_required(login_url='mainApp:login')
def send_message(request):
    if request.method == 'POST':
        #service = Service()
        form = UserMessagesform(request.POST, request.FILES)
        if form.is_valid():
            message=form.save(commit=False)
            message.sender = request.user.username
            message.save()
            #res = service.sendMessage(message.cleaned_data['id'], message.cleaned_data['sender'], message.cleaned_data['receiver'], message.cleaned_data['subject'], message.cleaned_data['content'], message.cleaned_data['creation_date'], message.cleaned_data['file'])
            return HttpResponseRedirect('/')
        else:
            form = UserMessagesform()
        return render(request, "inbox.html", {'form': form})   
