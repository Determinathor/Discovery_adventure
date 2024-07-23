from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline
from django.utils.html import format_html

from viewer.models import *
# Register your models here.


class ProductInline(TabularInline):
    model = Product.categories.through
    extra = 0
    verbose_name = 'Product'
    verbose_name_plural = 'Products'


class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'thumbnail_preview')
    inlines = [ProductInline]

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="/static/img/{}" width="50" height="50" />', obj.thumbnail)
        return "No Image"

    thumbnail_preview.short_description = 'Thumbnail Preview'


# admin.site.register(User)


admin.site.register(Manufacturer)
# admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Order)
# admin.site.register(Order_Line)
admin.site.register(Payment)