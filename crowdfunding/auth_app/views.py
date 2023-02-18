
from .models import *
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.rest import Client
from django.http import JsonResponse
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.http.response import HttpResponse
from django.http.response import HttpResponseRedirect
from .form import UserRegistrationForm

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
             user_image=r.FILES['user_image'],
         )
         return render(r,'login.html')
    else:
        return render(r,'register.html')

def login(r):
    if(r.method == 'POST'):
        usr = RegisterUser.objects.filter(
            user_email=r.POST['user_email'],
            user_password=r.POST['user_password'],
        ).first()
        if usr is not None:
            r.session['user_id'] = usr.user_id
            r.session['user_email'] = usr.user_email
            return redirect('index')
        else:
            Message = {}
            Message['Alert'] = 'username or password wrong'
            return render(r, 'index.html', Message)
    else:
        return render(r, 'login.html')

def logout(r):
    r.session.clear()
    return HttpResponseRedirect('login')

def view(r,key):
    view = RegisterUser.objects.filter(user_id=key)


#################

def regDjango(r):
    obj=RegisterUser.objects.get(user_id=1)

    Context = {
        'object': obj
    }
    return render(r,'registerDjango.html',Context)

def registerDjango(r):
    form = UserRegistrationForm(r.POST or None)
    if form.is_valid():
        form.save()

        Context = {
            'form':form
        }
        return render (r,'registerDjango.html', Context)
    else:
        return render(r, 'registerDjango.html', Context)

