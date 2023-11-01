from django.urls import path , include
from .import views
from accounts import views as Accountviews


urlpatterns = [
    path('', Accountviews.ven_dashbord , name='vendor'),
    path ('profile/', views.vprofile, name='vprofile'),
    path ('menue_builder/', views.menue_builder, name='menue_builder'),
    path ('menue_builder/category/<int:pk>', views.fooditems_by_category, name='fooditems_by_category'),
    
    
    # category CRUD
    path ('menue_builder/category/add', views.add_category, name='add_category'),
    path ('menue_builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path ('menue_builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    
    
    
    
]


