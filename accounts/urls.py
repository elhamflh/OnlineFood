from django.urls import path , include
from .import views

urlpatterns = [
    path('', views.my_account),
    path("registerUser/", views.registerUser, name= "registerUser"),
    path("registerVendor/", views.registerVendor, name= "registerVendor"),
    path("login/", views.login, name= "login"),
    path("logout/", views.logout, name= "logout"),
    path("myaccount/", views.my_account, name= "my_account"),
    path("custdashbord/", views.cus_dashbord, name= "custDashbord"),
    path("vendashbord/", views.ven_dashbord, name= "venDashbord"),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('forget_password/', views.forget_password, name='forget_password'),
    path('reset_password_validate/<uidb64>/<token>', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),
    
    path ('vendor/', include('vendor.urls')),
    path ('customer/', include('customers.urls')),
    
    
]


