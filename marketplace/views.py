from django.shortcuts import render , get_object_or_404
from vendor.models import Vendor
from menue.models import Category
from django.db.models import Prefetch
from menue.models import FoodItem
from django.http import HttpResponse , JsonResponse
from. models import Cart
from .context_processors import get_cart_counter , get_cart_amounts


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
    
    context = {
        'vendor' :vendor,
        'categories': categories,
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
            
        