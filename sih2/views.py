
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Product,Farmer_register,Transport_register
# Create your views here.
def index(request):
    return  render(request,"index.html")
def transport2(request):
    return render(request,"transport2.html")
def transport(request):
    if request.method=="POST":
        agency_name= request.POST['agency_name']
        transport_name= request.POST['transport_name']
        transport_lastname= request.POST['transport_lastname']
        transport_password= request.POST['transport_password']
        transport_confirmpassword= request.POST['transport_confirmpassword']
        transport_trucks=request.POST['transport_trucks']
        transport_number=request.POST['transport_number']
        transport_address=request.POST['transport_address']
        transport_address1=request.POST['transport_address1']
        transport_state=request.POST['transport_state']  
        transport_district=request.POST['transport_district']  
        transport_taluka=request.POST['transport_taluka']    
        transport_city=request.POST['transport_city'] 
        transport_code=request.POST['transport_code']
        transport_aadhar=request.POST['transport_aadhar']
        transport_gst=request.POST['transport_gst']
        aadhar=request.POST['myFile']
        if Transport_register.objects.filter(transportpassword=transport_password).exists():
            messages.info(request,'Password Taken')
            return redirect('transport')
        elif transport_password== transport_confirmpassword:
            if Transport_register.objects.filter(agencyname=agency_name).exists():
                messages.info(request,'Agency already registered')
                return redirect('transport')
            elif Transport_register.objects.filter(transportaadhar=transport_aadhar).exists():
                messages.info(request,'Already Registered Adhar Number')
                return redirect('transport')
            else:
                transport_user=Transport_register(agencyname=agency_name,transportname1=transport_name,transportname2=transport_lastname,transportpassword=transport_password,
                                              transporttruck=transport_trucks,transportcontact=transport_number,transportaddress=transport_address,
                                              transportaddress1=transport_address1,transportstate=transport_state,transportdistrict=transport_district,
                                              transporttaluka=transport_taluka,transportcity=transport_city,transportcode=transport_code,transportaadhar=transport_aadhar,
                                              transportgst=transport_gst,aadhar=aadhar
                                             )
                transport_user.save()
                user = User.objects.create_user(username=agency_name, password=transport_password, email="",first_name="",last_name="")
                user.save()
                print(agency_name)
                return redirect('transportlogin')
        else:
            return render(request,"transport.html")
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
            messages.info(request,'Invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')
def transportlogin(request):
    if request.method=='POST':
        agency_name=request.POST['agency_name']
        agency_password=request.POST['transport_password']
        user=auth.authenticate(username=agency_name,password=agency_password)
        if user is not None:
            auth.login(request,user)
            print(agency_password)
            return redirect('transport2')
        else:
            messages.info(request,'Invalid Credentials')
            print(agency_name)
            return render(request,'transportlogin.html')
    else:   
        return render(request,"transportlogin.html")
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
    if request.method=='POST':
        farmer_firstname= request.POST['first_name']
        farmer_lastname= request.POST['last_name']
        farmer_username= request.POST['user_name']
        farmer_password= request.POST['farmer_password']
        farmer_confirmpassword= request.POST['confirm_farmerpassword']
        farmer_email=request.POST['farmer_email']
        farmer_number=request.POST['farmer_no']
        farmer_address=request.POST['farmer_address']
        farmer_address1=request.POST['farmer_address1']
        farmer_state=request.POST['farmer_state']  
        farmer_district=request.POST['farmer_district']  
        farmer_taluka=request.POST['farmer_taluka']    
        farmer_city=request.POST['farmer_city'] 
        farmer_code=request.POST['farmer_code']

        if Farmer_register.objects.filter(password=farmer_password).exists():
            messages.info(request,'Password Taken')
            return redirect('farmerregister')
        # elif Farmer_register.objects.filter(email=farmer_email).exists():
        #     messages.info(request,'Email Already Taken')
        #     return redirect('farmerregister')
        elif farmer_password==farmer_confirmpassword:
            if Farmer_register.objects.filter(username=farmer_username).exists():
                messages.info(request,'Username Taken')
                return redirect('farmerregister')
            elif Farmer_register.objects.filter(email=farmer_email).exists():
                messages.info(request,'Email Taken')
                return redirect('farmerregister')
            else:   
                farmer_user = Farmer_register(firstname=farmer_firstname,lastname=farmer_lastname,username=farmer_username,
                                                                  password=farmer_password, confirmpassword=farmer_confirmpassword,email=farmer_email,
                                                                  contact_number=farmer_number,address=farmer_address,address1=farmer_address1,state=farmer_state,
                                                                  district=farmer_district,taluka=farmer_taluka,city=farmer_city,zipcode=farmer_code
                                                                  )
                farmer_user.save()
                user = User.objects.create_user(username=farmer_username, password=farmer_password, email=farmer_email,first_name="",last_name="")
                user.save()
                # print('Farmer Profile created')
                print(farmer_firstname)
                return redirect('farmerlogin')
        # else:
        #     messages.info(request,'password not matching..')    
        #     return redirect('farmerregister')
    return render(request,'farmerregister.html')



    # return render(request,"farmerregister.html")
def farmerlogin(request):
    if request.method=='POST':
        farmer_username= request.POST['user_name']
        farmer_password= request.POST['farmer_password']
        user = auth.authenticate(username=farmer_username,password=farmer_password)
        if user is not None:
            auth.login(request, user)
            return render(request,'farmerprofile.html')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('farmerlogin')
    else:
        return render(request,'farmerlogin.html')


    # return render(request,"farmerlogin.html")
def expertlogin(request):
    if request.method=='POST':
        expert_username=request.POST['expert_username']
        expert_password=request.POST['expert_password']
        user=auth.authenticate(username=expert_username,password=expert_password)
        if user is not None:
            auth.login(request,user)
            return redirect('experthome')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('expertlogin')
    else:
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
