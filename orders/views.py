from django.shortcuts import render , redirect
from marketplace.models import Cart
from marketplace.context_processors import get_cart_amounts
from .forms import OrderForm , Order
import json 
from .utils import generate_order_numbers
from django.http import HttpResponse
from orders.models import Payment , OrderedFood
from accounts.utils import send_notification
from django.contrib.auth.decorators import login_required
# Create your views here.


def place_order(request):
    cart_items = Cart.objects.filter(user= request.user).order_by("created_at")
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('marketplace')
    vendors_ids = []
    for i in cart_items:
        if i.fooditem.vendor.id not in vendors_ids:
            vendors_ids.append(i.fooditem.vendor.id)
            
    cart_amounts = get_cart_amounts(request)
    subtotal = cart_amounts.get('subtotal', 0)
    total_tax = cart_amounts.get('tax', 0)
    grand_total = cart_amounts.get('grand_total', 0)
    tax_data = cart_amounts.get('tax_dict', {})  #providing an empty dictionary as the default value.
    
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order()
            order.first_name= form.cleaned_data['first_name']
            order.last_name = form.cleaned_data['last_name']
            order.phone = form.cleaned_data['phone']
            order.email = form.cleaned_data['email']
            order.address = form.cleaned_data['address']
            order.country = form.cleaned_data['country']
            order.state = form.cleaned_data['state']
            order.city = form.cleaned_data['city']
            order.pin_code = form.cleaned_data['pin_code']
            order.user = request.user
            order.total = grand_total
            order.tax_data = json.dumps(tax_data)  #for changing the types like decimal to json(in model we have JsonFiels)
            order.total_tax = total_tax
            order.payment_method = request.POST['payment_method']
            order.save() # order id/ pk is generated
            order.order_number =generate_order_numbers(order.id) #1-first we save the form 2-then the id provide and 3-now we can get it
            order.save()
            context = {
                'order': order,
                }
        else:
            print(form.errors)
    return render(request, 'orders/place_order.html',context)

def payments(request):
    #CHECK IF THE REQUEST IS AJAX OR NOT
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'POST':
        # STORE THE PAYMENT DETAIL IN MODEL
        order_number = request.POST.grt('order_number')
        transaction_id = request.POST.grt('transaction_id')
        payment_method = request.POST.grt('payment_method')
        status = request.POST.grt('status')
        order = Order.objects.get(user=request.user, order_number=order_number)
        payment = Payment(
            user = request.user,
            transaction_id = transaction_id,
            status = status,
            payment_method = payment_method,
            amount = order.total,
        )
        payment.save()
        # UPDATE THE ORDER MODEL
        order.payment = payment
        order.is_ordered = True
        order.save()
        # MOVE THE CART ITEMS TO ORDERED FOOD MODEL
        cart_item = Cart.objects.filter(user = request.user)
        for item in cart_item:
            ordered_food = OrderedFood()
            ordered_food.order = order
            ordered_food.payment = payment
            ordered_food.user = request.user
            ordered_food.fooditem = item.fooditem
            ordered_food.quantity = item.quantity
            ordered_food.price = item.fooditem.price
            ordered_food.amount = item.fooditem.price * item.quantity # total amount
            ordered_food.save()
            return HttpResponse('save ordered food')
        # Send order configurtion email to the customer
        mail_subject = 'thank you for ordering with us'
        mail_template = ('order/order_configuration_email.html')
        context = {
            'user' : request.user,
            'order' : order,
            'to_email' : order.email,   
        }
        send_notification(mail_subject, mail_template , context)
        
         # Send order  reciving email to the vendor
        mail_subject = 'thank you for ordering with us'
        mail_template = ('order/order_configuration_email.html')
        to_email = []
        for i in cart_item:
            if i.fooditem.vendor.user.email not in to_email: 
                to_email.append(i.fooditem.vendor.user.email)
            context = {
                'order' : order,
                'to_email' : order.email,   
            }
            send_notification(mail_subject, mail_template , context)
 
            #CLEAR CART ITEMS AFTER SUCCESS PAYMENT
            cart_item.delete()
                
        # RETURN BACK TO AJAX WITH THE STATUS SUCCCESS OR FAILE      
        return HttpResponse ('Success') 
    return HttpResponse ('Payment view')
