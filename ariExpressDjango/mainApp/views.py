from django.http import HttpResponse
from django.shortcuts import render, redirect
import os
import sys
from ProjectCode.Service.Service import Service
from .forms import *
from ProjectCode.Service.Response import *


def startpage(request):
    return render(request, "startpage.html")

def mainpage(request):
    return render(request, 'mainpage.html')

def login(request):
    # service.logIn()
    msg = ""
    showMsg = False
    if request.method == 'POST':
        service = Service()
        # reg = service.register('asd', 'asd', 'asd')
        # print(reg.getReturnValue())
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # if username==""
            res = service.logIn(username, password)
            msg = res.getStatus()
            if res.getStatus() == True:
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
        form = registerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            res = service.register(username, password, email)
            msg = res.getReturnValue()
            # if res.getStatus() == True:
            #     return redirect('mainApp:login')
    else:
        form = registerForm()
        msg = ""
        showMsg = True


    return render(request, 'register.html', {'form': form,
                                          'msg': msg,
                                          'showMsg': showMsg})



def reset_password(request):
    pass

def homepage_guest(request):
    pass




def inbox(request):
    return render(request, 'inbox.html')