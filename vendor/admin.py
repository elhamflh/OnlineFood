from django.contrib import admin
from vendor.models import Vendor

class VendorAdmin(admin.ModelAdmin):
    list_display=('user','vendor_name', 'is_approved', 'created_at')

admin.site.register(Vendor,VendorAdmin)

# Register your models here.
