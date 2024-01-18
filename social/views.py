from django.shortcuts import render
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.contrib.auth import views
from . forms import *
from .models import *


# Create your views here.
#profile
def profile(reguest):
    return HttpResponse("پروفایل")


#Login
class UserLoginView(views.LoginView):
    form_class = LoginForm


#Logout
def Logout(request):
    return HttpResponse("خارج شدید!")
    
