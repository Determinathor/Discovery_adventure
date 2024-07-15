from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from viewer.models import *

# Registrace modelů do admin rozhraní

# Inline třída pro zobrazení produktů v rámci administrace kategorií
class ProductInline(TabularInline):
    model = Product.categories.through  # Definuje vztah M:N mezi Product a Category
    extra = 0  # Počet prázdných formulářů, které se zobrazí při přidávání nových položek
    verbose_name = 'Product'  # Jednotné číslo pro zobrazení v administraci
    verbose_name_plural = 'Products'  # Množné číslo pro zobrazení v administraci

# Třída pro správu kategorií v administraci
class CategoryAdmin(ModelAdmin):
    list_display = ['name',]  # Zobrazuje sloupec s názvem kategorie v seznamu
    inlines = [ProductInline]  # Zobrazuje produkty v rámci detailu kategorie

# Registrace modelů do administrace
admin.site.register(Manufacturer)  # Registrování modelu Manufacturer do admin rozhraní
admin.site.register(Product)  # Registrování modelu Product do admin rozhraní
admin.site.register(Cart)  # Registrování modelu Cart do admin rozhraní
admin.site.register(Category, CategoryAdmin)  # Registrování modelu Category s vlastní správou
admin.site.register(Order)  # Registrování modelu Order do admin rozhraní
admin.site.register(Order_Line)  # Registrování modelu Order_Line do admin rozhraní
admin.site.register(Payment)  # Registrování modelu Payment do admin rozhraní
