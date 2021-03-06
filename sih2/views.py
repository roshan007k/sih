
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import Product,Farmer_register,Transport_register, Order,Customer,OrderItem,ShippingAddress,ToDeliver,CompletedDeliveries,Comment,Transport_notifications,Farmer_notifications,Buyer_notifications

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

def profile_user(request):
    if request.user.is_authenticated:

        user1=request.user.get_username()
        user2=Customer.objects.filter(name=user1)
        print(user1)
        print(user2)
        if user2.exists():

            return render(request,'profile_user.html',{'user2':user2})
        else:
            return render(request,'profile_user.html')
    else:
        return render(request,'profile_user.html')
        
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
        farmer=product1.farmer.username
        farmer1=Farmer_register.objects.get(username=farmer)
        current_user = request.user
        
        #customer = Customer.objects.get(id=id)
    
        if Customer.objects.filter(id=id).exists():
            customer = Customer.objects.get(id=id)
            comment1 = Comment.objects.create(product = product1,farmer=farmer1, user = current_user, customer = customer, comment = comment, rate = rate, subject=subject)
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

    Transport_notifications.objects.create(
        farmer=farmer3.username,
        agencyname=data['shipping']['agencyname'],
        username=farmer3.username,
        firstname=farmer3.firstname,
        lastname=farmer3.lastname,
        password=farmer3.password,
        confirmpassword=farmer3.confirmpassword,
        email=farmer3.email,
        contact_number=farmer3.contact_number,
        address=farmer3.address,
        address1=farmer3.address1,
        state=farmer3.state,
        district=farmer3.district,
        taluka=farmer3.taluka,
        city=farmer3.city,
        zipcode=farmer3.zipcode
    )
    
    Agency1=Transport_register.objects.get(agencyname=data['shipping']['agencyname'])
    Farmer_notifications.objects.create(
        agencyname=Agency1.agencyname,
        transportname1=Agency1.transportname1,
        transportname2=Agency1.transportname2,
        transportpassword=Agency1.agencyname,
        transportcost=Agency1.transportcost,
        transporttruck=Agency1.transporttruck,
        transportcontact=Agency1.transportcontact,
        transportaddress=Agency1.transportaddress,
        transportaddress1=Agency1.transportaddress1,
        transportstate=Agency1.transportstate,
        transportdistrict=Agency1.transportdistrict,
        transporttaluka=Agency1.transporttaluka,
        transportcity=Agency1.transportcity,
        transportcode=Agency1.transportcode,
        transportaadhar=Agency1.transportaadhar,
        transportgst=Agency1.transportgst,
        aadhar = Agency1.aadhar

    )
    Buyer_notifications.objects.create(
        customer = customer,
        order = order,
        address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
        farmer=farmer3
    )

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
def transport_notifications(request):
    if request.user.is_authenticated:
        agency=request.user.get_username()
        user1=Transport_notifications.objects.filter(agencyname=agency)
    else:
        return redirect('transportlogin')


    return render(request,'transport_notifications.html',{'users':user1})
def farmer_notification(request):
    if request.user.is_authenticated:
        farmer=Farmer_register.objects.get(username=request.user)
        # farmer1 = get_object_or_404(farmer)
        user1=Buyer_notifications.objects.filter(farmer=farmer)
        print(user1)
    else:
        return redirect('farmerlogin')


    return render(request,'farmer_notification.html',{'users':user1})
def delivery_notification(request):
    if request.user.is_authenticated:
        farmer=Farmer_register.objects.get(username=request.user)
        user1=Transport_notifications.objects.get(farmer=farmer)
        user1=user1.agencyname
        user2=Farmer_notifications.objects.filter(agencyname=user1)
        
    else:
        return redirect('farmerlogin')


    return render(request,'delivery_notification.html',{'users':user2})

def display_farmerprofile(request, id):
    product = Product.objects.get(id = id)
    user2 = Farmer_register.objects.filter(username = product.farmer.username)
    products = Product.objects.filter(farmer = product.farmer)
    c = Comment.objects.filter(farmer = product.farmer)
    count = Comment.objects.filter(farmer = product.farmer).count()
    sum = 0
    for average in c:
        sum += average.rate
    average = sum/count
    print(average)
    return render(request, "display_farmerprofile.html", {'users':user2, 'products':products, 'c':c, 'average':average})


def update_farmer(request):
    user1=request.user.get_username()
    user2=Farmer_register.objects.filter(username=user1)
    if request.method=="POST":
        user3=Farmer_register.objects.get(username=user1)
        print(user3)
        if request.POST["name"]:
            user3.firstname=request.POST["name"]
            user3.save()
            print(user3.firstname)
        if request.POST["lastname"]:
            user3.lastname=request.POST["lastname"]
            user3.save()
        if request.POST["username"]:
            temp=User.objects.get(username=user1)
            temp.username=request.POST["username"]
            user3.username=request.POST["username"]
            user3.save()
            temp.save()
        if request.POST["email"]:
            user3.email=request.POST["email"]
            user3.save()
        if request.POST["contact"]:
            user3.contact_number=request.POST["contact"]
            user3.save()
        if request.POST["address"]:
            user3.address=request.POST["address"]
            user3.save()
        if request.POST["address1"]:
            user3.address1=request.POST["address1"]
            user3.save()
        if request.POST["state"]:
            user3.state=request.POST["state"]
            user3.save()
        if request.POST["district"]:
            user3.district=request.POST["district"]
            user3.save()
        if request.POST["taluka"]:
            user3.taluka=request.POST["taluka"]
            user3.save()
        if request.POST["city"]:
            user3.city=request.POST["city"]
            user3.save()
        if request.POST["zipcode"]:
            user3.zipcode=request.POST["zipcode"]
            user3.save()
        return render(request,'profile_farmer.html',{'user2':user2})
    else:
        return render(request,"update_farmer.html",{'user2':user2})
def update_transport(request):
    user1=request.user.get_username()
    user2=Transport_register.objects.filter(agencyname=user1)
    if request.method=="POST":
        user3=Transport_register.objects.get(agencyname=user1)
        print(user3)
        if request.POST["agencyname"]:
            temp=User.objects.get(username=user1)
            temp.username=request.POST["agencyname"]
            user3.agencyname=request.POST["agencyname"]
            user3.save()
            temp.save()
            print(user3.agencyname)
        if request.POST["transportname1"]:
            user3.transportname1=request.POST["transportname1"]
            user3.save()
        if request.POST["transportname2"]:
            user3.transportname2=request.POST["transportname2"]
            user3.save()
        if request.POST["transporttruck"]:
            user3.transporttruck=request.POST["transporttruck"]
            user3.save()
        if request.POST["transportcontact"]:
            user3.transportcontact=request.POST["transportcontact"]
            user3.save()
        if request.POST["transportaddress"]:
            user3.transportaddress=request.POST["transportaddress"]
            user3.save()
        if request.POST["transportaddress1"]:
            user3.transportaddress1=request.POST["transportaddress1"]
            user3.save()
        if request.POST["transportstate"]:
            user3.transportstate=request.POST["transportstate"]
            user3.save()
        if request.POST["transportdistrict"]:
            user3.transportdistrict=request.POST["transportdistrict"]
            user3.save()
        if request.POST["transporttaluka"]:
            user3.transporttaluka=request.POST["transporttaluka"]
            user3.save()
        if request.POST["transportcity"]:
            user3.transportcity=request.POST["transportcity"]
            user3.save()
        if request.POST["transportcode"]:
            user3.transportcode=request.POST["transportcode"]
            user3.save()
        if request.POST["transportaadhar"]:
            user3.transportaadhar=request.POST["transportaadhar"]
            user3.save()
        if request.POST["transportgst"]:
            user3.transportgst=request.POST["transportgst"]
            user3.save()
        if request.POST["transportcost"]:
            user3.transportcost=request.POST["transportcost"]
            user3.save()
        if request.POST["myFile"]:
            user3.aadhar=request.POST["myFile"]
            user3.save()
        return render(request,'profile_transport.html',{'user2':user2})
    else:
        return render(request,"update_transport.html",{'user2':user2})
