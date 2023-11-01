from vendor.models import Vendor
from django.shortcuts import get_object_or_404
from django.conf import settings

def get_vendor(request):
    try:
        vendor = get_object_or_404(Vendor,user=request.user)
    except:
        return None
    return dict(vendor=vendor)

# def get_google_api(request):
#     return {'GOOGLE_API_KEY': settings.GOOGLE_API_KEY}