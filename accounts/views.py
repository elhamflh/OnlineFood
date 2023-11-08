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
from.utils import send_verification_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from vendor.models import Vendor

# restric the vendor from accsesing the customer page
def check_role_vendor(user):
    if user.role ==1 :
        return True
    else:
        raise PermissionDenied


def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    

def registerUser(request):
    if request.method == 'POST':
        print(request.POST)
        form= UserForm(request.POST)
        
        if form.is_valid():
            #create user using create user form
            # password= form.cleaned_data['password'] #for hashing the password
            # user= form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # form.save()
            
            # Create the user using create_user method
            
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            
             # send verification user
            mail_subject = 'Activate ypur acccount'
            email_template = 'accounts/email/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
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
            
            # send verification user
            mail_subject = 'Activate ypur acccount'
            email_template = 'accounts/email/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Your account has been registered sucessfully! Please wait for the approval.')
            return redirect('home')
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

def activate(request, uidb64, token):
    # active the user by setting the is active is true 
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('my_account')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('my_account')
        

def login(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you already logged in!')
        return redirect('my_account')
    elif request.method == 'POST':
        email = request.POST['email']
        password= request.POST['password']
        
        user = auth.authenticate(email=email, password = password)
        
        if user is not None:
            auth.login(request,user)
            messages.success(request,'you are now login.')
            return redirect('my_account')
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
@user_passes_test(check_role_customer)
  
def cus_dashbord(request):
    return render (request,"accounts/cusDashbord.html")

@login_required(login_url ='login')
@user_passes_test(check_role_vendor)
def ven_dashbord(request):
    vendor = Vendor.objects.get(user = request.user)
    context={
        'vendor': vendor,
    }  
    return render (request,"accounts/venDashbord.html", context)


def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/email/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'Password reset link has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forget_password')
    return render(request, 'accounts/forget_password.html')


def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')