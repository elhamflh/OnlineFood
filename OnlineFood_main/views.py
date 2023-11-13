from django.shortcuts import render, redirect,get_object_or_404
from vendor.models import Vendor


def home(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active= True)[:8]
    context = {
        'vendors': vendors,
    }
    return render(request,'home.html', context)