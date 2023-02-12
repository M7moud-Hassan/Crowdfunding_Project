
from .models import *
from rest_framework.views import APIView
from twilio.rest import Client
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
# Create your views here.

def testTemp(r):
    return render(r, 'index.html')

def register(r):
    if(r.method=='POST'):
         RegisterUser.objects.create(
             first_name=r.POST['first_name'],
             last_name=r.POST['last_name'],
             user_email=r.POST['user_email'],
             user_password=r.POST['user_password'],
             user_mobile=r.POST['user_mobile'],
             user_image=r.POST['user_image'],
         )
         return render(r,'index.html')
    else:
        return render(r, 'register.html')

