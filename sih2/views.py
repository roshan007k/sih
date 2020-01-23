from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
def index(request):
    return  render(request,"index.html")
def transport2(request):
    return render(request,"transport2.html")
def transport(request):
    return render(request,"transport.html")
def login(request):
    return render(request,"login.html")
def transportlogin(request):
    return render(request,"transport-login.html")
def register(request):
    return render(request,"register.html")
def farmerregister(request):
    return render(request,"farmerregister.html")
def farmerlogin(request):
    return render(request,"farmerlogin.html")
def expertlogin(request):
    return render(request,"expertlogin.html")
def experthome(request):
    return render(request,"experthome.html")