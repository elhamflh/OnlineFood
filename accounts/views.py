from django.shortcuts import render , redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User , UserProfile
from vendor.forms import VendorForm
from django.contrib import messages
from django.contrib import auth
from .utils import detectUser
from django.contrib.auth.decorators import login_required , user_passes_test
from django.core.exceptions import PermissionDenied

# restric the vendor from accsesing the customer page

def check_role_custmer(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
def check_role_vendor(user):
    if user.role ==2 :
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
        form= UserForm(request.POST)
        
        if form.is_valid():
            #create user using create user form
            password= form.cleaned_data['password'] #for hashing the password
            user= form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            form.save()
            
            
            # Create the user using create_user method
            
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # username = form.cleaned_data['username']
            # email = form.cleaned_data['email']
            # password = form.cleaned_data['password']
            # user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            # user.role = User.CUSTOMER
            # user.save()
            messages.success(request,"your acount has been register succesfully!")
            return redirect('registerUser')
        else:
            print('invalid forms')
            print(form.errors)
    else:   
        form = UserForm
    context={
            'form': form,
        }
    return render (request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()

            # Send verification email
            # mail_subject = 'Please activate your account'
            # email_template = 'accounts/emails/account_verification_email.html'
            # send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Your account has been registered sucessfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)



def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you already logged in!')
        return redirect('dashbord')
    elif request.method == 'POST':
        email = request.POST['email']
        password= request.POST['password']
        
        user = auth.authenticate(email=email, password = password)
        
        if user is not None:
            auth.login(request,user)
            messages.success(request,'you are now login.')
            return redirect('dashbord')
        else:
            messages.error(request,'invalid login credentials.')
            return redirect('login')
    return render (request, "accounts/login.html")

def logout(request):
    auth.logout(request)
    messages.info(request,'you are now logout.')
    return redirect('login')
    
@login_required(login_url ='login')
  
def my_account(request):
    user= request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

@login_required(login_url ='login')
@user_passes_test(check_role_custmer)  
def cus_dashbord(request):
    return render (request,"accounts/cusDashbord.html")

@login_required(login_url ='login')
@user_passes_test(check_role_vendor)
def ven_dashbord(request):
    return render (request,"accounts/venDashbord.html")