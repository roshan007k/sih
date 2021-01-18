
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Product,Farmer_register,Transport_register, Order,Customer,OrderItem,ShippingAddress,ToDeliver,CompletedDeliveries,Comment
from django.conf import settings
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
import datetime
from . utils import CookieCart ,cartData,guestOrder
from django.core.serializers.json import DjangoJSONEncoder
# Create your views here.
relation=[]
def profile_farmer(request):
    if request.user.is_authenticated:

        user1=request.user.get_username()
        user2=Farmer_register.objects.filter(username=user1)
        if user2.exists():
            return render(request,'profile_farmer.html',{'user2':user2})
        else:
            return render(request,'profile_farmer.html')
    else:
        return render(request,'profile_farmer.html')
def profile_transport(request):
    if request.user.is_authenticated:

        user1=request.user.get_username()
        user2=Transport_register.objects.filter(agencyname=user1)
        print(user1)
        print(user2)
        if user2.exists():

            return render(request,'profile_transport.html',{'user2':user2})
        else:
            return render(request,'profile_transport.html')
    else:
        return render(request,'profile_transport.html')
def product(request, id):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    #product = Product.objects.filter(id=id)
    product1 = Product.objects.get(id=id)
    if request.method=='POST':
        subject = request.POST['subject']
        comment = request.POST['comment']
        rate = request.POST['rate']
        current_user = request.user
        
        #customer = Customer.objects.get(id=id)
    
        if Customer.objects.filter(id=id).exists():
            customer = Customer.objects.get(id=id)
            comment1 = Comment.objects.create(product = product1, user = current_user, customer = customer, comment = comment, rate = rate, subject=subject)
            comment1.save()
            messages.info(request, "Review Sent Successfully")
            c = Comment.objects.filter(product = product1)
            print(c)
            return render(request,"product.html", {'product':product1, 'cartItems' : cartItems, 'c' : c})
        else:
            messages.info(request, "Plz buy the product first")
            return render(request, "product.html", {'product':product1, 'cartItems' : cartItems})
    
    c = Comment.objects.filter(product = product1)
    return render(request,"product.html", {'product':product1, 'cartItems' : cartItems, 'c' : c})
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request, 'cart.html', context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    total_order=data['total']
    print(total_order)
    d={}
    if request.method=="POST":
        if request.user.is_authenticated:
            pass
        else:
            d["name"]=request.POST["name"]
            d["email"]=request.POST["email"]
        d["address"]=request.POST["address"]
        d["city"]=request.POST["city"]
        d["state"]=request.POST["state"]
        d["zipcode"]=request.POST["zipcode"]
        d=json.dumps(d)

        state1=request.POST["state"]
        state2=Transport_register.objects.filter(transportstate=state1)
        if state2.exists():
            context = {'items':items, 'order':order,'cartItems':cartItems,'states':state2,'total_order':total_order,'shipping':d}
        else:
            state2=Transport_register.objects.all()
            context = {'items':items, 'order':order,'cartItems':cartItems,'states':state2,'total_order':total_order,'shipping':d}
    else:
        context = {'items':items, 'order':order,'cartItems':cartItems,'total_order':total_order}
    #Create empty cart for now for non-logged in user
    return render(request,"checkout.html", context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False) 
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)
def index2(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    context ={'products':products,'cartItems':cartItems}
    return render(request,"index2.html",context)
def index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    products = Product.objects.all()
    context = {'products':products,'cartItems':cartItems, 'media_url':settings.MEDIA_URL}
    return  render(request,"index.html", context)
def transport2(request):
    return render(request,"transport2.html")
def transport(request):
    if request.method=="POST":
        agency_name= request.POST['agency_name']
        transport_name= request.POST['transport_name']
        transport_lastname= request.POST['transport_lastname']
        transport_password= request.POST['transport_password']
        transport_cost=request.POST['transport_cost']
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
                transport_user=Transport_register(agencyname=agency_name,transportname1=transport_name,transportname2=transport_lastname,transportpassword=transport_password,transportcost=transport_cost,
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
    return render(request,'login.html')
def transportlogin(request):
    if request.method=='POST':
        agency_name=request.POST['agency_name']
        agency_password=request.POST['transport_password']
        user=auth.authenticate(username=agency_name,password=agency_password)
        user1=Transport_register.objects.filter(agencyname=agency_name)
        if user is not None and user1.exists():
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
                user1 = User.objects.create_user(username=username, password=password, email=email,first_name="",last_name="")
                customer=Customer(user=user1,name=username,email=email,password=password)
                customer.save()
                user1.save()
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
        user1=Farmer_register.objects.all()
        if user is not None and user1.filter(username=farmer_username).exists():
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
        farmer=request.user.get_username()
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

        p = Product(farmer=farmer,name=productname,description=productdetails,price=productprice,product_type=foodtype,img=image)
        p.save()
        print(productname,productdetails,productprice,image,producttype)
    return render(request,"farmerprofile.html")
def logout(request):
    auth.logout(request)
    return redirect('/')

def processOrder(request):
    print("Data",request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer,order=guestOrder(request,data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        print(1)
        order.complete = True
    order.save()
    product1=OrderItem.objects.filter(order=order)
    for product in product1:
        product2=product.product
    farmer1=Product.objects.filter(name=product2)
    for farmer in farmer1:
        farmer3=farmer.farmer
        print(farmer3.username)
    buyer=Order.objects.filter(transaction_id=transaction_id)
    for customer2 in buyer:
        customer1=customer2.customer
        print(customer1)
    relation.append([farmer3.username,customer1])
    print(relation)
    # farmer1=Product.objects.filter(id=product_id)
    # for farmer in farmer1:
    #     farmer2=farmer.farmer
    # print(farmer2)
    ToDeliver.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
        agencyname=data['shipping']['agencyname']
		)
    ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
        agencyname=data['shipping']['agencyname']
		)

    return JsonResponse('Payment submitted..', safe=False)
def deliveries(request):
    if request.user.is_authenticated:
        user1=request.user.get_username()
        info=ToDeliver.objects.filter(agencyname=user1)
        if request.method=="POST":
            order_id=request.POST["order_id"]
            complete_order=ToDeliver.objects.get(order=order_id)
            CompletedDeliveries.objects.create(
                customer=complete_order.customer,
		        order=complete_order.order,
		        address=complete_order.address,
		        city=complete_order.city,
		        state=complete_order.state,
		        zipcode=complete_order.zipcode,
                agencyname=complete_order.agencyname

            )
            ToDeliver.objects.get(order=order_id).delete()
    else:
        return render(request,'transportlogin.html')
    context={'infos':info}
    return render(request,'deliveries.html',context)
def completeddeliveries(request):
    if request.user.is_authenticated:
        user1=request.user.get_username()
        info1=CompletedDeliveries.objects.filter(agencyname=user1)
    else:
        return render(request,"transportlogin.html")
    return render(request,'completeddeliveries.html',{"infos":info1})
def about(request):
    return render(request,'about.html')
def blog(request):
    return render(request,'blog.html')




