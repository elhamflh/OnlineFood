from vendor.models import Vendor ,UserProfile
from django.shortcuts import get_object_or_404
from django.conf import settings

def get_vendor(request):
    try:
        vendor = get_object_or_404(Vendor,user=request.user)
    except:
        vendor =  None
    return dict(vendor=vendor)

def get_user_profile(request):
    try:
        user_profile = get_object_or_404(UserProfile,user=request.user)
    except:
        user_profile= None
    return dict(user_profile=user_profile)

# def get_google_api(request):
#     return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}

def get_paypal_client_id(request):
    return {'PAYPAL_CLIENT_ID': settings.PAYPAL_CLIENT_ID}
