from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("login", views.loginuser, name='loginuser'),
    path("signin", views.signin, name='signinuser'),
    path("delete", views.delete, name='deleteuser'),
    path("authenticate", views.authenticate, name='authenticateuser'),
    path("logout", views.logoutuser, name='logoutuser')
]