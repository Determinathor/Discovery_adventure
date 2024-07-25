from django.db.models import Q
from django.shortcuts import render

from viewer.models import Order, Product


def cart_items_count(request):
    total_items = 0  # Default value

    if request.user.is_authenticated:
        # Zkontroluje, zda má user profil (pro případ nové databáze či restartu DB, creatusuperuser)
        if hasattr(request.user, 'profile'):
            try:
                order = Order.objects.get(User=request.user.profile, status='Pending')
                total_items = sum(item.quantity for item in order.order_line_set.all())
            except Order.DoesNotExist:
                total_items = 0
        else:
            # Handle case where user is authenticated but does not have a profile
            total_items = 0
    else:
        total_items = 0

    return {'cart_items_count': total_items}


def cart_status(request):
    has_items = False
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(User=request.user.profile, status='Pending')
            if order.order_line_set.exists():
                has_items = True
        except Order.DoesNotExist:
            pass
    return {'has_items': has_items}


def search_results(request):
    query = request.GET.get('q', '').strip()
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()  # Vracíme všechny produkty, pokud je pole prázdné

    return {
        'search_products': products,
        'search_query': query
    }