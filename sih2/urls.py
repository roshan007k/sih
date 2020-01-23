from django.urls import path

from . import views

urlpatterns = [

    path("",views.index,name='index'),
    path("transport2",views.transport2, name="transport2"),
    path("transport",views.transport, name="transport"),
    path("login",views.login, name="login"),
    path("transport-login",views.transportlogin, name="transport-login"),
    path("register",views.register, name="register"),
    path("farmerregister",views.farmerregister, name="farmerregister"),
    path("farmerlogin",views.farmerlogin, name="farmerlogin"),
    path("expertlogin",views.expertlogin, name="exxpertlogin"),
    path("experthome",views.experthome, name="experthome")
]