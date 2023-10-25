from vendor.models import Vendor
from django.shortcuts import get_object_or_404

def get_vendor(request):
    try:
        vendor = get_object_or_404(Vendor,user=request.user)
    except:
        return None
    return dict(vendor=vendor)