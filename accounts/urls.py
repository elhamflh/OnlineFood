from django.urls import path , include
from .import views

urlpatterns = [
    path("registerUser/", views.registerUser, name= "registerUser"),
    path("registerVendor/", views.registerVendor, name= "registerVendor"),
    path("login/", views.login, name= "login"),
    path("logout/", views.logout, name= "logout"),
    path("myaccount/", views.my_account, name= "my_account"),
    path("cusdashbord/", views.cus_dashbord, name= "cusDashbord"),
    path("vendashbord/", views.ven_dashbord, name= "venDashbord"),


    
]


