from django.http import HttpResponse
from django.shortcuts import render
import os
import sys
from ProjectCode.Service.Service import Service
from .forms import *
from ProjectCode.Service.Response import *


def homepage(request):
    return render(request, "homepage.html")

def login(request):
    # service.logIn()
    msg = ""
    showMsg = False
    if request.method == 'POST':
        service = Service()
        reg = service.register('asd', 'asd', 'asd')
        print(reg.getReturnValue())
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # if username==""
            res = service.logIn(username, password)
            msg = res.getReturnValue()
    else:
        form = loginForm()
        msg = ""
        showMsg = True


    return render(request, 'login.html', {'form': form,
                                          'msg': msg,
                                          'showMsg': showMsg})
    # return render(request, 'login.html')


def about(request):
    return HttpResponse('about')

def member(request):
    return render(request, 'member.html', 
                {'username': "Unknown",
                'email': "Unknown",
                'isLoggedIn': False
                })

def memberfound(request):
    service = Service()
    # service.openTheSystem("Ari")
    # data = service.getDjangoTestData()
    data = ("flexus", "flexus@gmail.com", "True")
    return render(request, 'member.html', 
                {'username': data[0],
                'email': data[1],
                'isLoggedIn': data[2]
                })

def register(request):
    service = Service()
    return render(request, 'register.html')


def reset_password(request):
    pass

def homepage_guest(request):
    pass