from django.urls import path

from . import views

urlpatterns = [

    path("",views.index,name='index'),
    path("transport2",views.transport2, name="transport2"),
    path("transport",views.transport, name="transport"),
    path("login",views.login, name="login"),
    path("logout",views.logout, name="logout"),
    path("transportlogin",views.transportlogin, name="transportlogin"),
    path("register",views.register, name="register"),
    path("farmerregister",views.farmerregister, name="farmerregister"),
    path("farmerlogin",views.farmerlogin, name="farmerlogin"),
    path("expertlogin",views.expertlogin, name="expertlogin"),
    path("experthome",views.experthome, name="experthome"),
    path("farmerprofile",views.farmerprofile, name="farmerprofile"),
    path("index2",views.index2, name="index2"),
    path("cart",views.cart, name="cart"),
    path("checkout",views.checkout, name="checkout"),
    path("product",views.product, name="product"),
    path("update_item",views.updateItem, name="update_item"),
    path("processOrder",views.processOrder, name= "processOrder"),
    path("deliveries",views.deliveries, name= "deliveries"),
    path("completeddeliveries",views.completeddeliveries, name= "completeddeliveries"),
    path("about",views.about, name="about"),
    path("blog",views.blog, name="blog"),
    path("profile_farmer",views.profile_farmer, name="profile_farmer"),
    path("profile_transport",views.profile_transport, name="profile_transport")
]