from django.shortcuts import render , get_object_or_404 , redirect
from vendor.models import Vendor , OpeningHour
from menue.models import Category
from django.db.models import Prefetch
from menue.models import FoodItem
from django.http import HttpResponse , JsonResponse
from. models import Cart
from django.db.models import Q
from .context_processors import get_cart_counter , get_cart_amounts
from datetime import date , datetime
from orders.forms import OrderForm
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active= True)
    vondor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vondor_count,
    }
    
    return render(request,"marketplace/listing.html", context )

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    
    #prefetch is for when we want to access the food Items from category model
    #but we dont have foodItem forigen key. so we write "related_name" on foodItem model
    #and then connect it with Category model by prefetch_related.
    categories = Category.objects.filter(vendor=vendor).prefetch_related( 
        Prefetch(
            'fooditem',
            queryset = FoodItem.objects.filter(is_available=True)
        ))
    opening_hours = OpeningHour.objects.filter(vendor=vendor).order_by('day', '-from_hour')
    today_date = date.today()
    today= today_date.isoweekday()
    current_opening_hours= OpeningHour.objects.filter(vendor=vendor , day=today)
    
            
   
    context = {
        'vendor' :vendor,
        'categories': categories,
        'opening_hours': opening_hours,
        'current_opening_hours': current_opening_hours,
        
    }
    return render ( request , 'marketplace/vendor_detail.html',context)

def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                #check if the food item is exist or not
                fooditem= FoodItem.objects.get(id=food_id)
                try:
                    # check if that item already added by user
                    chkCart = Cart.objects.get(user=request.user ,fooditem=fooditem)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': "success", 'message':"Increase the cart quantity.", 'cart_counter':get_cart_counter(request), 'qty': chkCart.quantity , 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user , fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': "success", 'message':"Food were added to the cart", 'cart_counter':get_cart_counter(request), 'qty': chkCart.quantity , 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': "Failed", 'message':"this food item dosen't exixt!"})
        else:      
            return JsonResponse({'status': "success", 'message':"Invalid request!"})
    else:
        return JsonResponse({'status': "login_required", 'message':"please login to continue."})
    
    
def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                #check if the food item is exist or not
                fooditem = FoodItem.objects.get(id=food_id)
                try:
                    # check if that item already added by user
                    chkCart = Cart.objects.get(user=request.user , fooditem=fooditem)
                    # decreas the cart quantity
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0   
                    return JsonResponse({'status': "success", 'message':"Increase the cart quantity.", 'cart_counter':get_cart_counter(request), 'qty': chkCart.quantity , 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': "Failed", 'message':" You don't have this item in your cart"})
            except:
                return JsonResponse({'status': "Failed", 'message':"this food item dosen't exixt!"})
        else:      
            return JsonResponse({'status': "success", 'message':"Invalid request!"})
    else:
        return JsonResponse({'status': "login_required", 'message':"please login to continue."})
    
    
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context={
        'cart_items':cart_items,
    }
    return render (request,'marketplace/cart.html', context)

def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                cart_item = Cart.objects.get(user=request.user, id =cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status': "succcess", 'message':"The food item has been deleted!",'cart_counter':get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                  return JsonResponse({'status': "Failed", 'message':"The food item dosen't exixt!"})
        else:
              return JsonResponse({'status': "Failed", 'message':"Invalied request!"})
            
            
def search(request):
    # if not 'address' in request.GET:
    #     return redirect('marketplace')
    # else:
        address = request.GET['address']
        latitude = request.GET['lat']
        longitude = request.GET['lng']
        radius = request.GET['radius']
        keyword = request.GET['keyword']

        # get vendor ids that has the food item the user is looking for
        fetch_vendors_by_fooditems = FoodItem.objects.filter(food_title__icontains=keyword, is_available=True).values_list('vendor', flat=True)
        
        vendors = Vendor.objects.filter(Q(id__in=fetch_vendors_by_fooditems) | Q(vendor_name__icontains=keyword, is_approved=True, user__is_active=True))
        
        vendor_count = vendors.count()
        context = {
            'vendors': vendors,
            'vendor_count': vendor_count,
        }


        return render(request, 'marketplace/listing.html', context)
    
@login_required(login_url='login')   
def checkout(request):
    cart_items = Cart.objects.filter(user= request.user).order_by("created_at")
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'phone': request.user.phone_number,
        'email': request.user.email,
        'address': user_profile.address,
        'country': user_profile.country,
        'state': user_profile.state,
        'city': user_profile.city,
        'pin_code': user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)  #initial is for setting default values from customer profile to theirs bills.
    context = {
        'form': form,
        'cart_items': cart_items

    }
    return render(request, 'marketplace/checkout.html', context)