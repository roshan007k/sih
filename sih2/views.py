
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Product
# Create your views here.
def index(request):
    return  render(request,"index.html")
def transport2(request):
    return render(request,"transport2.html")
def transport(request):
    return render(request,"transport.html")
def login(request):
    if  request.method== 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')
def transportlogin(request):
    return render(request,"transport-login.html")
def register(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        confirmpassword= request.POST['confirmpassword']
        email = request.POST['email']

        if password==confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:   
                user = User.objects.create_user(username=username, password=password, email=email,first_name="",last_name="")
                user.save()
                print('user created')
                return redirect('login')

        else:
            messages.info(request,'password not matching..')    
            return redirect('register')
        return redirect('/')
        
    else:
        return render(request,'register.html')
def farmerregister(request):
    return render(request,"farmerregister.html")
def farmerlogin(request):
    return render(request,"farmerlogin.html")
def expertlogin(request):
    return render(request,"expertlogin.html")
def experthome(request):
    return render(request,"experthome.html")
def farmerprofile(request):
    if  request.method== 'POST':
        foodtype=0
        productname= request.POST['productname']
        productdetails = request.POST['productdetails']
        productprice=request.POST['productprice']
        image=request.POST['image']
        producttype=request.POST['producttype']
        if(producttype=='Food'):
            foodtype=1
        elif(producttype=='Cash'):
            foodtype=2
        elif(producttype=='Plantation'):
            foodtype=3
        else:
            foodtype=4

        p = Product(name=productname,description=productdetails,price=productprice,product_type=foodtype,img=image)
        p.save()
        print(productname,productdetails,productprice,image,producttype)
    return render(request,"farmerprofile.html")
def logout(request):
    auth.logout(request)
    return redirect('/')
