from django.shortcuts import render, redirect, HttpResponse
from app1.models import Contact
from app1.models import Totpkey
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate as auth
from django.contrib import messages
import pyotp
import qrcode
import requests
import json


# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    context ={
        'variable' : 'Jeet'
    }
    return render(request, 'index.html')

def about(request):
    context={
        'variable': "abc",
        'a' : 322
    }
    return render(request, 'about.html', context)
     
def contact(request):
    if request.method == "POST":
        email=request.POST.get('email')
        desc=request.POST.get('desc')
        contact=Contact(email=email, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, "Your Message is Sent")
    return render(request, 'contact.html')

def loginuser(request):
    if not(request.user.is_anonymous):
        return redirect("/") 
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = auth(username=username, password=password)
        if (user is not None):
            # ReCaptcha
            clientKey=request.POST['g-recaptcha-response']
            secretKey="" # Place your ReCaptcha Secret Key
            cData={
                'secret': secretKey,
                'response': clientKey
            }
            r=requests.post('https://www.google.com/recaptcha/api/siteverify',data=cData)
            response=json.loads(r.text)
            bot=response['success']

            # Bypassing 2FA for admin account
            if username=="admin":
                login(request, user)
                return redirect("/")
        # otp verification
            otp=request.POST.get('otp')
            key=Totpkey.objects.filter(username=username)[0].key
            totp=pyotp.totp.TOTP(key)
            if totp.verify(otp) and bot:
                login(request, user)
                return redirect("/")
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')

def logoutuser(request):
    print(request.user.id)
    logout(request)
    return redirect("/login")

def signin(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        user = User.objects.filter(username=username)

        # reCaptcha
        clientKey=request.POST['g-recaptcha-response']
        secretKey="" # Place your ReCaptcha Secret Key
        cData={
            'secret': secretKey,
            'response': clientKey
        }
        r=requests.post('https://www.google.com/recaptcha/api/siteverify',data=cData)
        response=json.loads(r.text)
        bot=response['success']

        if not(user.exists()) and password1==password2 and bot:
            key=pyotp.random_base32()
            otp=pyotp.totp.TOTP(key)
            uri=otp.provisioning_uri(name=request.POST.get('username'), issuer_name='AppByJeet')
            qrcode.make(uri).save("./static/otp.png")
            request.session['key'] = key
            request.session['username'] = username
            request.session['password'] = password1
            return redirect("/authenticate")
    return render(request, 'signin.html')

def delete(request):
    if (not(request.user.is_anonymous) and request.user.username != "admin"):
        username=request.user
        user = User.objects.get(username = username)
        user.delete()
        # delete otp key
        Totpkey.objects.filter(username=username)[0].delete()
    return redirect("/login")

def authenticate(request):
    try:
        key=request.session['key']
        username=request.session['username']
        password=request.session['password']
        otp=pyotp.totp.TOTP(key)
    except:
        return HttpResponse("Error 401: Unauthorized")
    context={
        'key': key
    }
    if otp.verify(request.POST.get('otp')):
        totpkey=Totpkey(username=username,key=key)
        totpkey.save()
        user = User.objects.create_user(username,"",password)
        return redirect("/login")
    # else:
    #     messages.error(request, "Incorrect OTP")
    return render(request, 'authentication.html',context)
