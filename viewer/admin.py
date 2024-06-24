from django.contrib import admin

from viewer.models import *
# Register your models here.

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Manufacturer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Order_Line)
admin.site.register(Payment)


