from viewer.models import Order


def cart_items_count(request):
    total_items = 0

    #if request.user.is_authenticated:
    #    try:
    #        order = Order.objects.get(User=request.user.profile, status='Pending')
    #        total_items = sum(item.quantity for item in order.order_line_set.all())
    #    except Order.DoesNotExist:
    #        total_items = 0
    #else:
    #    total_items = 0
    #    -->

    return {'cart_items_count': total_items}