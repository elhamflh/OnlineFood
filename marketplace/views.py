from django.shortcuts import render , get_object_or_404
from vendor.models import Vendor
from menue.models import Category
from django.db.models import Prefetch
from menue.models import FoodItem
from django.http import HttpResponse , JsonResponse
from. models import Cart
from .context_processors import get_cart_counter


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
            'fooditems',
            queryset = FoodItem.objects.filter(is_available=True)
        ))
    
    context = {
        'vendor' :vendor,
        'categories': categories,
    }
    return render ( request , 'marketplace/vendor_detail.html',context)

def add_to_cart(request,food_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                #check if the food item is exist or not
                foodItem= FoodItem.objects.get(id=food_id)
                try:
                    # check if that item already added by user
                    chkCart = Cart.objects.get(user=request.user , food_id=food_id)
                    # Increase the cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': "success", 'message':"Increase the cart quantity.", 'cart_counter':get_cart_counter(request), 'qty': chkCart.quantity})
                except:
                    chkCart = Cart.objects.create(user=request.user , food_id=food_id, quantity=1)
                    return JsonResponse({'status': "success", 'message':"Food were added to the cart"})
            except:
                return JsonResponse({'status': "Failed", 'message':"this food item dosen't exixt!"})
        else:      
            return JsonResponse({'status': "success", 'message':"Invalid request!"})
    else:
        return JsonResponse({'status': "login_required", 'message':"please login to continue."})
    
    
def decrease_cart(request,food_id):
    if request.user.is_authenticated:
        if request.is_ajax():
            try:
                #check if the food item is exist or not
                foodItem= FoodItem.objects.get(id=food_id)
                try:
                    # check if that item already added by user
                    chkCart = Cart.objects.get(user=request.user , food_id=food_id)
                    # decreas the cart quantity
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0   
                    return JsonResponse({'status': "success", 'message':"Increase the cart quantity.", 'cart_counter':get_cart_counter(request), 'qty': chkCart.quantity})
                except:
                    return JsonResponse({'status': "Failed", 'message':" You don't have this item in your cart"})
            except:
                return JsonResponse({'status': "Failed", 'message':"this food item dosen't exixt!"})
        else:      
            return JsonResponse({'status': "success", 'message':"Invalid request!"})
    else:
        return JsonResponse({'status': "login_required", 'message':"please login to continue."})
    