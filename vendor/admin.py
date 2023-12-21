from django.contrib import admin
from vendor.models import Vendor , OpeningHour


class OpeningHourAdmin(admin.ModelAdmin):
    list_display=('vendor','day','from_hour', 'to_hour',"is_closed")
class VendorAdmin(admin.ModelAdmin):
    list_display=('user','vendor_name', 'is_approved', 'created_at')
    list_display_links= ('user','vendor_name')
    
    
admin.site.register(Vendor,VendorAdmin)
admin.site.register(OpeningHour,OpeningHourAdmin)

# Register your models here.
