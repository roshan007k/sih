import json
from .models import *

def cartData(request):
    if request.user.is_authenticated:
        cookieData = CookieCart(request)
        total=cookieData['total']
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = CookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        total=cookieData['total']
    return {'cartItems':cartItems,'order':order,'items':items,'total':total}

def CookieCart(request):
    total=0
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    items = []
    order = {'get_cart_total' : 0, 'get_cart_items' : 0}
    cartItems = order['get_cart_items']
    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total=0
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            item = {
                    'id':product.id,
                    'product':{'id':product.id,'name':product.name, 'price':product.price, 
                    'img':product.img}, 'quantity':cart[i]['quantity'],
                    'get_total':total,
                }
            items.append(item)
        except:
            pass
    return {'items':items, 'order':order,'cartItems':cartItems,'total':total}
def guestOrder(request,data):
    print('User is not logged in')
    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    cookieData = CookieCart(request)
    items = cookieData['items']
    customer, created = Customer.objects.get_or_create(
            email=email,
        )
    customer.name = name
    customer.save()
    order = Order.objects.create(
            customer=customer,
            complete=False,
		)
    for item in items:
        product = Product.objects.get(id=item['id'])
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity'],
            )
    return(customer,order)