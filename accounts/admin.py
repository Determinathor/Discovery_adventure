from django.contrib import admin

from accounts.models import Profile
from viewer.models import Order_Line, Order, Product


class OrderLineInline(admin.TabularInline):
    model = Order_Line
    extra = 1
    readonly_fields = ['total_order_line_price']
    fields = ('Product', 'product_price', 'quantity', 'total_order_line_price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_cost', 'delivery_address', 'date_of_sale', 'status', 'User')
    inlines = [OrderLineInline]


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_order_id', 'Product', 'quantity')

    def get_user(self, obj):
        return obj.Order.User.user.username
    get_user.short_description = 'User'
    get_user.admin_order_field = 'Order__User__user__username'  # Allows column ordering

    def get_order_id(self, obj):
        return obj.Order.id
    get_order_id.short_description = 'Order ID'
    get_order_id.admin_order_field = 'Order__id'  # Allows column ordering



admin.site.register(Order, OrderAdmin)

admin.site.register(Order_Line, OrderLineAdmin)
admin.site.register(Product)
admin.site.register(Profile)