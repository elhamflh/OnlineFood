from django.urls import path , include
from accounts import views as AccountViwes
from . import views

urlpatterns = [
    path('',AccountViwes.cus_dashbord, name="customer"),
    path('profile/',views.cprofile, name="cprofile"),
    #MY_ORDERS
    path('my_orders/', views.my_orders, name="customer_my_orders"),
    path('order_detail/<int:order_number>/', views.order_detail, name="order_detail"),
    
    
    
]