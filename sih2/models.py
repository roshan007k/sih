from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm
# Create your models here.
class Farmer_register(models.Model):
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    username=models.CharField(max_length=50,unique=True)
    password=models.CharField(max_length=100)
    confirmpassword=models.CharField(max_length=100)
    email=models.EmailField(max_length=254,unique=True)
    contact_number=models.CharField(max_length=100,unique=True)
    address=models.TextField(max_length=200)
    address1=models.TextField(max_length=200,blank=True)
    state=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    taluka=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    zipcode=models.CharField(max_length=50)

    def __str__(self):
	    return self.username
class Transport_register(models.Model):
    agencyname=models.CharField(max_length=100)
    transportname1=models.CharField(max_length=100)
    transportname2=models.CharField(max_length=100)
    transportpassword=models.CharField(max_length=50)
    transportcost=models.BigIntegerField()
    transporttruck=models.BigIntegerField()
    transportcontact=models.BigIntegerField()
    transportaddress=models.CharField(max_length=200)
    transportaddress1=models.CharField(max_length=200)
    transportstate=models.CharField(max_length=50)
    transportdistrict=models.CharField(max_length=50)
    transporttaluka=models.CharField(max_length=50)
    transportcity=models.CharField(max_length=50)
    transportcode=models.BigIntegerField()
    transportaadhar=models.BigIntegerField()
    transportgst=models.BigIntegerField()
    aadhar = models.ImageField(upload_to='images/')
class Product(models.Model):
    FoodGrains = 1
    CashCrops = 2
    PlantationCrops = 3
    HorticultureCrops = 4
    PRODUCT_TYPES = (
        (FoodGrains, 'Food'),
        (CashCrops, 'Cash'),
        (PlantationCrops, 'Plantation'),
        (HorticultureCrops, 'Horticulture'),
    )
    farmer=models.ForeignKey(Farmer_register,on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    img = models.ImageField(null=True, blank=True)
    product_type = models.PositiveSmallIntegerField(choices=PRODUCT_TYPES)
    timestamp = models.DateField(auto_now_add=True, auto_now=False)
    
    def __str__(self):
	    return self.name



class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)
    password=models.CharField(max_length=200,default=1)

    def __str__(self):  
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
	    return str(self.id)

    # @property
    # def shipping(self):
    #     shipping = False
    #     orderitems = self.orderitem_set.all()
    #     for i in orderitems:
    #         if i.product.digital == False:
    #             shipping = True
    #     return shipping
    
    @property
    def get_cart_total(self):
	    orderitems = self.orderitem_set.all()
	    total = sum([item.get_total for item in orderitems])
	    return total 

    @property
    def get_cart_items(self):
	    orderitems = self.orderitem_set.all()
	    total = sum([item.quantity for item in orderitems])
	    return total

class OrderItem(models.Model):
    farmer=models.ForeignKey(Farmer_register,on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
	    total = self.product.price * self.quantity
	    return total
    
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    agencyname=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.address
class CompletedDeliveries(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    agencyname=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.address
class ToDeliver(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    agencyname=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.address
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=250, blank=True)
    comment = models.CharField(max_length=250, blank=True)
    rate = models.IntegerField(default = 1)
    timestamp = models.DateField(auto_now_add=True, auto_now=False)
    class Meta:
        ordering=['-id']
    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']

class Transport_notifications(models.Model):
    farmer=models.CharField(max_length=100,null=True)
    agencyname=models.CharField(max_length=50,null=True)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=100)
    confirmpassword=models.CharField(max_length=100)
    email=models.EmailField(max_length=254)
    contact_number=models.CharField(max_length=100)
    address=models.TextField(max_length=200)
    address1=models.TextField(max_length=200,blank=True)
    state=models.CharField(max_length=50)
    district=models.CharField(max_length=50)
    taluka=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    zipcode=models.CharField(max_length=50)

    def __str__(self):
        return self.username
class Farmer_notifications(models.Model):
    agencyname=models.CharField(max_length=100,null=True)
    transportname1=models.CharField(max_length=100)
    transportname2=models.CharField(max_length=100)
    transportpassword=models.CharField(max_length=50)
    transportcost=models.BigIntegerField()
    transporttruck=models.BigIntegerField()
    transportcontact=models.BigIntegerField()
    transportaddress=models.CharField(max_length=200)
    transportaddress1=models.CharField(max_length=200)
    transportstate=models.CharField(max_length=50)
    transportdistrict=models.CharField(max_length=50)
    transporttaluka=models.CharField(max_length=50)
    transportcity=models.CharField(max_length=50)
    transportcode=models.BigIntegerField()
    transportaadhar=models.BigIntegerField()
    transportgst=models.BigIntegerField()
    aadhar = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.agencyname
    
class Buyer_notifications(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    farmer=models.ForeignKey(Farmer_register,on_delete=models.SET_NULL, null=True)

    # def __str__(self):
    #     return self.customer
    
