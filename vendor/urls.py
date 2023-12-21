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
    
    # food CRUD
    path ('menue_builder/food/add', views.add_food, name='add_food'),
    path ('menue_builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path ('menue_builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),
    
    # opening_hour
    path('opening_hours/', views.opening_hours, name="opening_hour"),
    path('opening_hours/add/', views.add_opening_hours, name="add_opening_hours"),
    path('opening_hours/remove/<int:pk>/', views.remove_opening_hour, name="remove_opening_hour"),
    
    
    # VENDOR_ORDER_DETAIL
    path('order_detail/<int:order_number>/', views.order_detail, name="vendor_order_detail"),
    
    
    
]


