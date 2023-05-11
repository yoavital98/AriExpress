from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as loginFunc
from django.contrib.auth import logout as logoutFunc, authenticate
from django.contrib.auth.forms import UserCreationForm
import os
import sys
from ProjectCode.Service.Service import Service
from .forms import *
from ProjectCode.Service.Response import *
from django.contrib.auth.models import User



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
                form.save()
                username = form.cleaned_data['username']
                password = form.cleaned_data['password1']
                email = form.cleaned_data['email']
                print("ok")
                res = service.register(username, password, email)
                msg = res.getReturnValue()
                if res.getStatus() == True:
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
    service = Service()
    return render(request, 'myshops.html', {})
    

def reset_password(request):
    pass

def homepage_guest(request):
    pass




def inbox(request):
    return render(request, 'inbox.html')