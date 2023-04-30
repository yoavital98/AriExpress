from django.http import HttpResponse
from django.shortcuts import render
import os
import sys
sys.path.append(f"{os.getcwd()}/../../")
from ProjectCode.Service.Service import Service


def homepage(request):
    # return HttpResponse('homepage')
    return render(request, 'homepage.html')


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