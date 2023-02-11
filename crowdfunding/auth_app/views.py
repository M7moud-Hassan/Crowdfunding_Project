import random

from django.shortcuts import render
from rest_framework.views import APIView
from twilio.rest import Client
from django.http import JsonResponse
# Create your views here.
class sendOTP(APIView):
    def post(self, r):
        account_sid = "AA"
        auth_token = "ASA"
        number = r.data['number']
        client = Client(account_sid, auth_token)
        otp = generateOTP()
        body = "Your OTP is"+ str(otp)
        message = client.messages.create(from_= "Abdelnasser ", body = body, to = number )
        if message.sid:
            print("send Successfull")
            return JsonResponse({"success": True})
        else:
            print("Send fail")
            return JsonResponse({"success": False})
def generateOTP():
    return random.randrange(1000000,9999999)


