from django.contrib import admin

from accounts.models import Profile
from viewer.models import Order_Line, Order, Product


class OrderLineInline(admin.TabularInline):
    model = Order_Line
    extra = 1
    readonly_fields = ['total_order_line_price']
    fields = ('Product', 'product_price', 'quantity', 'total_order_line_price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'User', 'total_cost', 'status', 'date_of_sale')
    list_filter = ('status', 'date_of_sale')
    search_fields = ('User__username', 'status')
    ordering = ('-date_of_sale',)
    list_per_page = 10
    inlines = [OrderLineInline]


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_user', 'get_order_id', 'Product', 'quantity')
    ordering = ('-Order',)
    list_per_page = 10

    def get_user(self, obj):
        return obj.Order.User.user.username
    get_user.short_description = 'User'
    get_user.admin_order_field = 'Order__User__user__username'  # umožní řazení

    def get_order_id(self, obj):
        return obj.Order.id
    get_order_id.short_description = 'Order ID'
    get_order_id.admin_order_field = 'Order__id'  # řazení


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'stock', 'manufacturer', 'product_type')
    list_filter = ('product_type', 'manufacturer')
    search_fields = ('title', 'manufacturer__name')
    ordering = ('title',)
    list_per_page = 20


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'user_username', 'phone_number')
    search_fields = ('user__username', 'email')
    list_per_page = 20

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'

    def user_username(self, obj):
        return obj.user.username

    user_username.short_description = 'Username'


admin.site.register(Order, OrderAdmin)
admin.site.register(Order_Line, OrderLineAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Profile, ProfileAdmin)