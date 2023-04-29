from django.http import HttpResponse
from django.shortcuts import render



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
    return render(request, 'member.html', 
                {'username': "Unknown",
                'email': "Unknown",
                'isLoggedIn': False
                })