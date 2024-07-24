from django.db.models import Q
from django.shortcuts import render

from viewer.models import Order, Product


def cart_items_count(request):
    total_items = 0
    # if request.user.is_authenticated:
    #     try:
    #         order = Order.objects.get(User=request.user.profile, status='Pending')
    #         total_items = sum(item.quantity for item in order.order_line_set.all())
    #     except Order.DoesNotExist:
    #         total_items = 0
    # else:
    #     total_items = 0

    return {'cart_items_count': total_items}


def search_results(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.none()  # Vracíme prázdný QuerySet místo všech produktů

    return {
        'search_products': products,
        'search_query': query
    }